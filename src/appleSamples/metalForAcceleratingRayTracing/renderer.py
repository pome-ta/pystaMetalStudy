from pathlib import Path
import ctypes

from objc_util import ObjCClass, create_objc_class, ObjCInstance, on_main_thread

from mScene import createCube, vertices, colors, normals, masks
from transforms import matrix4x4_translation, matrix4x4_rotation, matrix4x4_scale
from simd.vector3 import Vector3
from pyTypes import Uniforms
#from simd.matrix4 import Matrix4
import pdbg

root_path = Path(__file__).parent
header_path = root_path / Path('./ShaderTypes.h')
shader_path = root_path / Path('./Shaders.metal')

maxFramesInFlight = 3
alignedUniformsSize = (ctypes.sizeof(Uniforms) + 255) & ~255  # 255

rayStride = 48

# import -> Scene.h
FACE_MASK_NONE = 0
FACE_MASK_NEGATIVE_X = (1 << 0)
FACE_MASK_POSITIVE_X = (1 << 1)
FACE_MASK_NEGATIVE_Y = (1 << 2)
FACE_MASK_POSITIVE_Y = (1 << 3)
FACE_MASK_NEGATIVE_Z = (1 << 4)
FACE_MASK_POSITIVE_Z = (1 << 5)
FACE_MASK_ALL = ((1 << 6) - 1)

TRIANGLE_MASK_GEOMETRY = 1
TRIANGLE_MASK_LIGHT = 2
RAY_MASK_PRIMARY = 3
RAY_MASK_SHADOW = 1
RAY_MASK_SECONDARY = 1

MTLPixelFormatRGBA16Float = 115
MTLPixelFormatRGBA32Float = 125
MTLTextureType2D = 2

MTLStorageModeShared = 0
MTLResourceStorageModeShift = 4

MTLResourceStorageModeShared = MTLStorageModeShared << MTLResourceStorageModeShift

MTLStorageModePrivate = 2
MTLResourceStorageModePrivate = MTLStorageModePrivate << MTLResourceStorageModeShift

err_ptr = ctypes.c_void_p()


class MPSIntersectionDistancePrimitiveIndexCoordinates(ctypes.Structure):
  _fields_ = [
    ('distance', ctypes.c_float),
    ('primitiveIndex', ctypes.c_uint32),
    ('coordinates', ctypes.c_float * 2),
  ]


intersectionStride = ctypes.sizeof(
  MPSIntersectionDistancePrimitiveIndexCoordinates)

class Renderer:
  def __init__(self):
    self.view: MTKView
    self.device: MTLDevice
    self.queue: MTLCommandQueue
    self.library: MTLLibrary

    self.accelerationStructure: MPSTriangleAccelerationStructure
    self.intersector: MPSRayIntersector

    self.vertexPositionBuffer: MTLBuffer
    self.vertexNormalBuffer: MTLBuffer
    self.vertexColorBuffer: MTLBuffer
    self.rayBuffer: MTLBuffer
    self.shadowRayBuffer: MTLBuffer
    self.intersectionBuffer: MTLBuffer
    self.uniformBuffer: MTLBuffer
    self.triangleMaskBuffer: MTLBuffer

    self.rayPipeline: MTLComputePipelineState
    self.shadePipeline: MTLComputePipelineState
    self.shadowPipeline: MTLComputePipelineState
    self.accumulatePipeline: MTLComputePipelineState
    self.copyPipeline: MTLComputePipelineState

  def initWithMetalKitView_(self, _view):
    self.view = _view
    self.device = self.view.device()
    #print(f'Metal device: {self.device.name()}')

    self.loadMetal()
    self.createPipelines()
    self.createScene()
    self.createBuffers()
    self.createIntersector()

  def loadMetal(self):
    self.view.colorPixelFormat = MTLPixelFormatRGBA16Float
    self.view.sampleCount = 1
    # xxx: size?
    self.view.drawableSize = self.view.frame().size

    # --- load shader code
    header = header_path.read_text('utf-8')
    shader = shader_path.read_text('utf-8')
    source = header + shader

    MTLCompileOptions = ObjCClass('MTLCompileOptions')
    options = MTLCompileOptions.new()
    self.library = self.device.newLibraryWithSource_options_error_(
      source, options, err_ptr)
    self.queue = self.device.newCommandQueue()

  def createPipelines(self):
    computeDescriptor = ObjCClass(
      'MTLComputePipelineDescriptor').alloc().init()

    computeDescriptor.threadGroupSizeIsMultipleOfThreadExecutionWidth = 1

    rayKernel = self.library.newFunctionWithName_('rayKernel')
    computeDescriptor.computeFunction = rayKernel

    self.rayPipeline = self.device.newComputePipelineStateWithDescriptor_options_reflection_error_(
      computeDescriptor, 0, err_ptr, err_ptr)

    shadeKernel = self.library.newFunctionWithName_('shadeKernel')
    computeDescriptor.computeFunction = shadeKernel

    self.shadePipeline = self.device.newComputePipelineStateWithDescriptor_options_reflection_error_(
      computeDescriptor, 0, err_ptr, err_ptr)

    shadowKernel = self.library.newFunctionWithName_('shadowKernel')
    computeDescriptor.computeFunction = shadowKernel

    self.shadowPipeline = self.device.newComputePipelineStateWithDescriptor_options_reflection_error_(
      computeDescriptor, 0, err_ptr, err_ptr)

    accumulateKernel = self.library.newFunctionWithName_('accumulateKernel')
    computeDescriptor.computeFunction = accumulateKernel

    self.accumulatePipeline = self.device.newComputePipelineStateWithDescriptor_options_reflection_error_(
      computeDescriptor, 0, err_ptr, err_ptr)

    renderDescriptor = ObjCClass('MTLRenderPipelineDescriptor').alloc().init()

    renderDescriptor.sampleCount = self.view.sampleCount()

    copyVertex = self.library.newFunctionWithName_('copyVertex')
    renderDescriptor.vertexFunction = copyVertex

    copyFragment = self.library.newFunctionWithName_('copyFragment')
    renderDescriptor.fragmentFunction = copyFragment

    renderDescriptor.colorAttachments().objectAtIndexedSubscript(
      0).pixelFormat = self.view.colorPixelFormat()

    self.copyPipeline = self.device.newRenderPipelineStateWithDescriptor_error_(
      renderDescriptor, err_ptr)

  def createScene(self):
    transform = matrix4x4_translation(0.0, 1.0, 0.0) * matrix4x4_scale(
      0.5, 1.98, 0.5)
    createCube(FACE_MASK_POSITIVE_Y,
               Vector3(1.0, 1.0, 1.0), transform, True, TRIANGLE_MASK_LIGHT)
    #print(transform)

  def createBuffers(self):
    # Uniform buffer contains a few small values which change from frame to frame. We will have up to 3 frames in flight at once, so allocate a range of the buffer for each frame. The GPU will read from one chunk while the CPU writes to the next chunk. Each chunk must be aligned to 256 bytes on macOS and 16 bytes on iOS.
    # 均一バッファには、フレームごとに変化するいくつかの小さな値が含まれています。 一度に最大3つのフレームが飛行するため、フレームごとにバッファの範囲を割り当てます。  GPUは1つのチャンクから読み取り、CPUは次のチャンクに書き込みます。 各チャンクは、macOSでは256バイト、iOSでは16バイトに揃える必要があります。
    uniformBufferSize = alignedUniformsSize * maxFramesInFlight

    # Vertex data should be stored in private or managed buffers on discrete GPU systems (AMD, NVIDIA). Private buffers are stored entirely in GPU memory and cannot be accessed by the CPU. Managed buffers maintain a copy in CPU memory and a copy in GPU memory.
    # 頂点データは、ディスクリートGPUシステム（AMD、NVIDIA）のプライベートバッファまたは管理バッファに保存する必要があります。 プライベートバッファは完全にGPUメモリに格納され、CPUによってアクセスできない。 管理バッファーは、CPUメモリとGPUメモリのコピーをコピーしてください。

    # https://tech.ckme.co.jp/cpp/cpp_predef.shtml
    # xxx: not だから、`MTLResourceStorageModeShared` ?
    '''
    #if !TARGET_OS_IPHONE
      options = MTLResourceStorageModeManaged;
    #else
      options = MTLResourceStorageModeShared;
    #endif
    '''
    options = MTLResourceStorageModeShared
    self.uniformBuffer = self.device.newBufferWithLength_options_(
      uniformBufferSize, options)

    # Allocate buffers for vertex positions, colors, and normals. Note that each vertex position is a float3, which is a 16 byte aligned type.
    # 頂点の位置、色、法線にバッファを割り当てます。 各頂点位置はfloat3であることに注意してください。これは、16バイトに整列されたタイプです。
    self.vertexPositionBuffer = self.device.newBufferWithLength_options_(
      len(vertices) * ctypes.sizeof(Vector3), options)

    self.vertexColorBuffer = self.device.newBufferWithLength_options_(
      len(colors) * ctypes.sizeof(Vector3), options)

    self.vertexNormalBuffer = self.device.newBufferWithLength_options_(
      len(normals) * ctypes.sizeof(Vector3), options)

    self.triangleMaskBuffer = self.device.newBufferWithLength_options_(
      len(masks) * ctypes.sizeof(ctypes.c_uint32), options)

    ctypes.memmove(self.vertexPositionBuffer.contents(),
                   ctypes.byref(vertices[0]),
                   self.vertexPositionBuffer.length())
    ctypes.memmove(self.vertexColorBuffer.contents(),
                   ctypes.byref(colors[0]), self.vertexColorBuffer.length())
    ctypes.memmove(self.vertexNormalBuffer.contents(),
                   ctypes.byref(normals[0]), self.vertexNormalBuffer.length())
    ctypes.memmove(self.triangleMaskBuffer.contents(),
                   ctypes.byref(ctypes.c_uint32(masks[0])),
                   self.triangleMaskBuffer.length())

  def createIntersector(self):
    MPSRayIntersector = ObjCClass('MPSRayIntersector')
    self.intersector = MPSRayIntersector.alloc().initWithDevice_(self.device)
    self.intersector.rayDataType = 2  # MPSRayDataTypeOriginMaskDirectionMaxDistance
    self.intersector.rayStride = rayStride
    self.intersector.rayMaskOptions = 1  #MPSRayMaskOptionPrimitive

    MPSTriangleAccelerationStructure = ObjCClass(
      'MPSTriangleAccelerationStructure')

    self.accelerationStructure = MPSTriangleAccelerationStructure.alloc(
    ).initWithDevice_(self.device)
    self.accelerationStructure.vertexBuffer = self.vertexPositionBuffer
    self.accelerationStructure.maskBuffer = self.triangleMaskBuffer
    self.accelerationStructure.triangleCount = int(len(vertices) / 3)

    #self.accelerationStructure.rebuild()
    #pdbg.state(self.accelerationStructure)

  def renderer_init(self):
    # todo: MTKViewDelegate func
    def mtkView_drawableSizeWillChange_(_self, _cmd, _view, _size):
      rayCount = int(_size.width * _size.height)

      self.rayBuffer = self.device.newBufferWithLength_options_(
        rayStride * rayCount, MTLResourceStorageModePrivate)
      self.shadowRayBuffer = self.device.newBufferWithLength_options_(
        rayStride * rayCount, MTLResourceStorageModePrivate)
      self.intersectionBuffer = self.device.newBufferWithLength_options_(
        intersectionStride * rayCount, MTLResourceStorageModePrivate)

      renderTargetDescriptor = ObjCClass('MTLTextureDescriptor').alloc().init()
      renderTargetDescriptor.pixelFormat = MTLPixelFormatRGBA32Float
      renderTargetDescriptor.textureType = MTLTextureType2D
      #renderTargetDescriptor.setWidth_(_size.width)
      #renderTargetDescriptor.height = int(_size.height)
      #renderTargetDescriptor.height = int(_size.height())
      pdbg.state(renderTargetDescriptor)
      print(_size.height)

    def drawInMTKView_(_self, _cmd, _view):
      view = ObjCInstance(_view)
      commandBuffer = self.queue.commandBuffer()

    PyRenderer = create_objc_class(
      name='PyRenderer',
      methods=[drawInMTKView_, mtkView_drawableSizeWillChange_],
      protocols=['MTKViewDelegate'])
    return PyRenderer.new()


if __name__ == '__main__':
  from gameViewController import GameViewController
  gv = GameViewController()

