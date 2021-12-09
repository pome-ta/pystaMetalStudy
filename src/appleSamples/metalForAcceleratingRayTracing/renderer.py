from pathlib import Path
import ctypes

from objc_util import ObjCClass

from transforms import matrix4x4_translation, matrix4x4_rotation, matrix4x4_scale
#from simd.matrix4 import Matrix4
import pdbg

root_path = Path(__file__).parent
header_path = root_path / Path('./ShaderTypes.h')
shader_path = root_path / Path('./Shaders.metal')

err_ptr = ctypes.c_void_p()
MTLPixelFormatRGBA16Float = 115

TRIANGLE_MASK_GEOMETRY = 1
TRIANGLE_MASK_LIGHT = 2
RAY_MASK_PRIMARY = 3
RAY_MASK_SHADOW = 1
RAY_MASK_SECONDARY = 1

FACE_MASK_NONE = 0
FACE_MASK_NEGATIVE_X = (1 << 0)
FACE_MASK_POSITIVE_X = (1 << 1)
FACE_MASK_NEGATIVE_Y = (1 << 2)
FACE_MASK_POSITIVE_Y = (1 << 3)
FACE_MASK_NEGATIVE_Z = (1 << 4)
FACE_MASK_POSITIVE_Z = (1 << 5)
FACE_MASK_ALL = ((1 << 6) - 1)


class Renderer:
  def __init__(self):
    self.view: MTKView
    self.device: MTLDevice
    self.queue: MTLCommandQueue
    self.library: MTLLibrary

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

  def createBuffers(self):
    pass


if __name__ == '__main__':
  from gameViewController import GameViewController
  gv = GameViewController()

