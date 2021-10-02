from math import sin, cos, tan
from pathlib import Path
import ctypes

from objc_util import c, create_objc_class, ObjCClass, ObjCInstance, nsurl, ns
import ui

import pdbg

MTLCreateSystemDefaultDevice = c.MTLCreateSystemDefaultDevice
MTLCreateSystemDefaultDevice.argtypes = []
MTLCreateSystemDefaultDevice.restype = ctypes.c_void_p


MTKModelIOVertexDescriptorFromMetal = c.MTKModelIOVertexDescriptorFromMetal
MTKModelIOVertexDescriptorFromMetal.argtypes = [ctypes.c_void_p]
MTKModelIOVertexDescriptorFromMetal.restype = ctypes.c_void_p

   

shader_path = Path('./Resources/Shaders.metal')

err_ptr = ctypes.c_void_p()


Position = (ctypes.c_float * 3)
Color = (ctypes.c_float * 4)
Texture = (ctypes.c_float * 2)


class float3(ctypes.Structure):
  _fields_ = [
    ('x', ctypes.c_float),
    ('y', ctypes.c_float),
    ('z',ctypes.c_float)
  ]

  def __str__(self):
    fstr = f'''float3:
      [x:{self.x: .4f}
       y:{self.y: .4f}
       z:{self.z: .4f}]
    '''
    return fstr


class f4(ctypes.Structure):
  _fields_ = [
    ('ffff', ctypes.c_float * 4),
  ]


class float_xyzw(ctypes.Structure):
  _fields_ = [
    ('x', ctypes.c_float),
    ('y', ctypes.c_float),
    ('z', ctypes.c_float),
    ('w', ctypes.c_float),
  ]


class float4(ctypes.Union):
  _anonymous_ = [
    ('xyzw'),
    ('ffff'),
  ]
  _fields_ = [('xyzw', float_xyzw), ('ffff', f4)]

  def __init__(self, x, y, z, w):
    self.x = x
    self.y = y
    self.z = z
    self.w = w


class columns(ctypes.Structure):
  _fields_ = [
    ('c0', float4),
    ('c1', float4),
    ('c2', float4),
    ('c3', float4),
  ]


class float16(ctypes.Structure):
  _fields_ = [
    ('m', (ctypes.c_float * 16)),
  ]


# https://github.com/Cethric/OpenGLES-Pythonista/blob/master/GLKit/glkmath/matrix4.py
class m16(ctypes.Structure):
  _fields_ = [
    ('m00', ctypes.c_float), ('m01', ctypes.c_float), ('m02', ctypes.c_float), ('m03', ctypes.c_float),
    
    ('m10', ctypes.c_float), ('m11', ctypes.c_float), ('m12', ctypes.c_float), ('m13', ctypes.c_float),
    
    ('m20', ctypes.c_float), ('m21', ctypes.c_float), ('m22', ctypes.c_float), ('m23', ctypes.c_float),
    
    ('m30', ctypes.c_float), ('m31', ctypes.c_float), ('m32', ctypes.c_float), ('m33', ctypes.c_float),
  ]
 

class matrix_float4x4(ctypes.Union):
  _anonymous_ = [
    ('columns'),
    ('s1'),
    ('s2'),
  ]
  _fields_ = [
    ('columns', columns),
    ('s1', float16),
    ('s2', m16),
  ]

  def __str__(self):
    valus = [float(x) for x in self.s1.m]
    mstr = f'''matrix_float4x4:
      [{valus[0]:.4f}, {valus[1]:.4f}, {valus[2]:.4f}, {valus[3]:.4f}]
      [{valus[4]:.4f}, {valus[5]:.4f}, {valus[6]:.4f}, {valus[7]:.4f}]
      [{valus[8]:.4f}, {valus[9]:.4f}, {valus[10]:.4f}, {valus[11]:.4f}]
      [{valus[12]:.4f}, {valus[13]:.4f}, {valus[14]:.4f}, {valus[15]:.4f}]'''
    return mstr

  def __init__(self):
    # xxx: `matrix_identity_float4x4` ?
    columns = (
      float4(1.0, 0.0, 0.0, 0.0),
      float4(0.0, 1.0, 0.0, 0.0),
      float4(0.0, 0.0, 1.0, 0.0),
      float4(0.0, 0.0, 0.0, 1.0))
    self.columns = columns

  @staticmethod
  def translation_x_y_z_(x, y, z):
    columns = (
      float4(1.0, 0.0, 0.0, 0.0),
      float4(0.0, 1.0, 0.0, 0.0),
      float4(0.0, 0.0, 1.0, 0.0),
      float4(  x,   y,   z, 1.0))
    matrix = matrix_float4x4()
    matrix.columns = columns
    return matrix

  @staticmethod
  def scale_x_y_z_(x, y, z):
    columns = (
      float4(  x, 0.0, 0.0, 0.0),
      float4(0.0,   y, 0.0, 0.0),
      float4(0.0, 0.0,   z, 0.0),
      float4(0.0, 0.0, 0.0, 1.0))
    matrix = matrix_float4x4()
    matrix.columns = columns
    return matrix

  @staticmethod
  def rotation_angle_x_y_z_(angle, x, y, z):
    c = cos(angle)
    s = sin(angle)

    column0 = float4(0.0, 0.0, 0.0, 0.0)
    column0.x = x * x + (1.0 - x * x) * c
    column0.y = x * y * (1.0 - c) - z * s
    column0.z = x * z * (1.0 - c) + y * s
    column0.w = 0.0

    column1 = float4(0.0, 0.0, 0.0, 0.0)
    column1.x = x * y * (1.0 - c) + z * s
    column1.y = y * y + (1.0 - y * y) * c
    column1.z = y * z * (1.0 - c) - x * s
    column1.w = 0.0

    column2 = float4(0.0, 0.0, 0.0, 0.0)
    column2.x = x * z * (1.0 - c) - y * s
    column2.y = y * z * (1.0 - c) + x * s
    column2.z = z * z + (1.0 - z * z) * c
    column2.w = 0.0

    column3 = float4(0.0, 0.0, 0.0, 1.0)

    matrix = matrix_float4x4()
    columns = (column0, column1, column2, column3)
    matrix.columns = columns
    return matrix

def translationMatrix(position):
  x, y, z = position
  translateMatrix = matrix_float4x4.translation_x_y_z_(x, y, z)
  return matrix_multiply(matrix_float4x4(), translateMatrix)

def scalingMatrix(scale):
  x, y, z = scale
  scaledMatrix = matrix_float4x4.scale_x_y_z_(x, y, z)
  return matrix_multiply(matrix_float4x4(), scaledMatrix)

def rotationMatrix(angle, axis):
  x, y, z = axis
  rotationMatrix = matrix_float4x4.rotation_angle_x_y_z_(angle, x, y, z)
  return matrix_multiply(matrix_float4x4(), rotationMatrix)


def projectionMatrix(*args):
  nearZ, farZ, aspect, fov = args
  y = 1 / tan(fov * 0.5)
  x = y / aspect
  z = farZ / (nearZ - farZ)
  columns = (
    float4(  x, 0.0, 0.0, 0.0),
    float4(0.0,   y, 0.0, 0.0),
    float4(0.0, 0.0,   z, -1.0),
    float4(0.0, 0.0,   z * nearZ, 0.0))
  matrix = matrix_float4x4()
  matrix.columns = columns
  return matrix


# https://github.com/Cethric/OpenGLES-Pythonista/blob/master/GLKit/glkmath/matrix4.py
def matrix_multiply(matrixLeft, matrixRight):
  matrix = matrix_float4x4()
  matrix.m[
    0] = matrixLeft.m[0] * matrixRight.m[0] + matrixLeft.m[4] * matrixRight.m[1] + matrixLeft.m[8] * matrixRight.m[2] + matrixLeft.m[12] * matrixRight.m[3]
  matrix.m[
    4] = matrixLeft.m[0] * matrixRight.m[4] + matrixLeft.m[4] * matrixRight.m[5] + matrixLeft.m[8] * matrixRight.m[6] + matrixLeft.m[12] * matrixRight.m[7]
  matrix.m[
    8] = matrixLeft.m[0] * matrixRight.m[8] + matrixLeft.m[4] * matrixRight.m[9] + matrixLeft.m[8] * matrixRight.m[10] + matrixLeft.m[12] * matrixRight.m[11]
  matrix.m[
    12] = matrixLeft.m[0] * matrixRight.m[12] + matrixLeft.m[4] * matrixRight.m[13] + matrixLeft.m[8] * matrixRight.m[14] + matrixLeft.m[12] * matrixRight.m[15]

  matrix.m[
    1] = matrixLeft.m[1] * matrixRight.m[0] + matrixLeft.m[5] * matrixRight.m[1] + matrixLeft.m[9] * matrixRight.m[2] + matrixLeft.m[13] * matrixRight.m[3]
  matrix.m[
    5] = matrixLeft.m[1] * matrixRight.m[4] + matrixLeft.m[5] * matrixRight.m[5] + matrixLeft.m[9] * matrixRight.m[6] + matrixLeft.m[13] * matrixRight.m[7]
  matrix.m[
    9] = matrixLeft.m[1] * matrixRight.m[8] + matrixLeft.m[5] * matrixRight.m[9] + matrixLeft.m[9] * matrixRight.m[10] + matrixLeft.m[13] * matrixRight.m[11]
  matrix.m[
    13] = matrixLeft.m[1] * matrixRight.m[12] + matrixLeft.m[5] * matrixRight.m[13] + matrixLeft.m[9] * matrixRight.m[14] + matrixLeft.m[13] * matrixRight.m[15]

  matrix.m[
    2] = matrixLeft.m[2] * matrixRight.m[0] + matrixLeft.m[6] * matrixRight.m[1] + matrixLeft.m[10] * matrixRight.m[2] + matrixLeft.m[14] * matrixRight.m[3]
  matrix.m[
    6] = matrixLeft.m[2] * matrixRight.m[4] + matrixLeft.m[6] * matrixRight.m[5] + matrixLeft.m[10] * matrixRight.m[6] + matrixLeft.m[14] * matrixRight.m[7]
  matrix.m[
    10] = matrixLeft.m[2] * matrixRight.m[8] + matrixLeft.m[6] * matrixRight.m[9] + matrixLeft.m[10] * matrixRight.m[10] + matrixLeft.m[14] * matrixRight.m[11]
  matrix.m[
    14] = matrixLeft.m[2] * matrixRight.m[12] + matrixLeft.m[6] * matrixRight.m[13] + matrixLeft.m[10] * matrixRight.m[14] + matrixLeft.m[14] * matrixRight.m[15]

  matrix.m[
    3] = matrixLeft.m[3] * matrixRight.m[0] + matrixLeft.m[7] * matrixRight.m[1] + matrixLeft.m[11] * matrixRight.m[2] + matrixLeft.m[15] * matrixRight.m[3]
  matrix.m[
    7] = matrixLeft.m[3] * matrixRight.m[4] + matrixLeft.m[7] * matrixRight.m[5] + matrixLeft.m[11] * matrixRight.m[6] + matrixLeft.m[15] * matrixRight.m[7]
  matrix.m[
    11] = matrixLeft.m[3] * matrixRight.m[8] + matrixLeft.m[7] * matrixRight.m[9] + matrixLeft.m[11] * matrixRight.m[10] + matrixLeft.m[15] * matrixRight.m[11]
  matrix.m[
    15] = matrixLeft.m[3] * matrixRight.m[12] + matrixLeft.m[7] * matrixRight.m[13] + matrixLeft.m[11] * matrixRight.m[14] + matrixLeft.m[15] * matrixRight.m[15]

  return matrix

class Uniforms(ctypes.Structure):
  _fields_ = [
    ('modelViewProjectionMatrix', matrix_float4x4),
  ]



class Renderer:
  def __init__(self, view):
    self.view = view
    self.device = view.device()
    
    #self.device = None
    self.commandQueue = None
    self.library = None
    self.renderPipelineState = None
    self.uniformsBuffer = None
    self.meshes = None
    self.texture = None
    self.depthStencilState = None
    # xxx: あとで事前に作る
    self.vertexDescriptor = ObjCClass('MTLVertexDescriptor').new()

    self.view.setClearColor_((0.5, 0.5, 0.5, 1))
    self.view.setColorPixelFormat_(80)
    self.initializeMetalObjects()
    self.createMatrixAndBuffers()
    self.createLibraryAndRenderPipeline()
    self.createAsset()
    #pdbg.state(self.view)
    
    

  def initializeMetalObjects(self):
    #MTLCreateSystemDefaultDevice = c.MTLCreateSystemDefaultDevice
    #MTLCreateSystemDefaultDevice.argtypes = []
    #MTLCreateSystemDefaultDevice.restype = ctypes.c_void_p

    #device = ObjCInstance(MTLCreateSystemDefaultDevice())
    commandQueue = self.device.newCommandQueue()
    self.view.setDepthStencilPixelFormat_(260)  # depth32Float_stencil8
    descriptor = ObjCClass('MTLDepthStencilDescriptor').new()
    descriptor.setDepthCompareFunction_(1)  # .less
    descriptor.setDepthWriteEnabled_(1)  # true
    depthStencilState = self.device.newDepthStencilStateWithDescriptor_(descriptor)
    
    #self.device = device
    self.commandQueue = commandQueue
    self.depthStencilState = depthStencilState
    
  def createMatrixAndBuffers(self):
    scaled = scalingMatrix((1, 1, 1))
    rotated = rotationMatrix(90, (0, 1, 0))
    translated = translationMatrix((0, -10, 0))
    modelMatrix = matrix_multiply(matrix_multiply(translated, rotated), scaled)
    cameraPosition = (0, 0, -50)
    viewMatrix = translationMatrix(cameraPosition)
    aspect = self.view.drawableSize().width / self.view.drawableSize().height
    projMatrix = projectionMatrix(0.1, 100, aspect, 1)
    modelViewProjectionMatrix = matrix_multiply(projMatrix, matrix_multiply(viewMatrix, modelMatrix))
    #self.uniformsBuffer = self.device.newBufferWithLength_options_(ctypes.sizeof(matrix_float4x4), 0)
    # xxx: あとでやる
    
    self.mvpMatrix = Uniforms()
    self.mvpMatrix.modelViewProjectionMatrix = modelViewProjectionMatrix
    
    
    self.uniformsBuffer = self.device.newBufferWithBytes_length_options_(ctypes.byref(self.mvpMatrix), ctypes.sizeof(matrix_float4x4), 0)
    
    
  def createLibraryAndRenderPipeline(self):
    source = shader_path.read_text('utf-8')
    library = self.device.newLibraryWithSource_options_error_(source, err_ptr, err_ptr)
    
    vert_func = library.newFunctionWithName_('vertex_func')
    frag_func = library.newFunctionWithName_('fragment_func')
    
    # --- step 1: set up the render pipeline state
    self.vertexDescriptor.attributes().objectAtIndexedSubscript_(0).offset = 0
    self.vertexDescriptor.attributes().objectAtIndexedSubscript_(0).format = 30  # float3
    self.vertexDescriptor.attributes().objectAtIndexedSubscript_(1).offset = 12
    self.vertexDescriptor.attributes().objectAtIndexedSubscript_(1).format = 3  # uchar4
    self.vertexDescriptor.attributes().objectAtIndexedSubscript_(2).offset = 16
    self.vertexDescriptor.attributes().objectAtIndexedSubscript_(2).format = 25  # half2
    self.vertexDescriptor.attributes().objectAtIndexedSubscript_(3).offset = 20
    self.vertexDescriptor.attributes().objectAtIndexedSubscript_(3).format = 28  # float
    self.vertexDescriptor.layouts().objectAtIndexedSubscript(0).stride = 24
    
    renderPipelineDescriptor = ObjCClass('MTLRenderPipelineDescriptor').new()
    renderPipelineDescriptor.vertexDescriptor = self.vertexDescriptor
    renderPipelineDescriptor.vertexFunction = vert_func
    renderPipelineDescriptor.fragmentFunction = frag_func
    
    renderPipelineDescriptor.colorAttachments().objectAtIndexedSubscript(0).pixelFormat = 80  # .bgra8Unorm
    renderPipelineDescriptor.stencilAttachmentPixelFormat = self.view.depthStencilPixelFormat()
    
    self.renderPipelineState = self.device.newRenderPipelineStateWithDescriptor_error_(renderPipelineDescriptor, err_ptr)
    
  def createAsset(self):
    # --- step 2: set up the asset initialization
    desc = ObjCInstance(MTKModelIOVertexDescriptorFromMetal(self.vertexDescriptor))
    
    attribute = desc.attributes().objectAtIndexedSubscript_(0)
    attribute.setName_('MDLVertexAttributePosition')
    attribute = desc.attributes().objectAtIndexedSubscript_(1)
    attribute.setName_('MDLVertexAttributeColor')
    attribute = desc.attributes().objectAtIndexedSubscript_(2)
    attribute.setName_('MDLVertexAttributeTextureCoordinate')
    attribute = desc.attributes().objectAtIndexedSubscript_(3)
    attribute.setName_('MDLVertexAttributeOcclusionValue')
    
    mtkBufferAllocator = ObjCClass('MTKMeshBufferAllocator').new().initWithDevice_(self.device)
    
    url = Path('./Resources/Farmhouse.obj')
    
    asset = ObjCClass('MDLAsset').new().initWithURL_vertexDescriptor_bufferAllocator_(nsurl(str(url)), desc, mtkBufferAllocator)
    
    
    loader = ObjCClass('MTKTextureLoader').new()
    loader.initWithDevice_(self.device)
    file = Path('./Resources/Farmhouse.png').absolute()
    
    self.texture = loader.newTextureWithContentsOfURL_options_error_(nsurl(str(file)), err_ptr, err_ptr)
    
    # --- step 3: set up MetalKit mesh and submesh objects
    
    mesh = asset.objectAtIndexedSubscript_(0)
    mesh.generateAmbientOcclusionVertexColorsWithQuality_attenuationFactor_objectsToConsider_vertexAttributeNamed_(1.0, 0.98, [mesh], 'MDLVertexAttributeOcclusionValue')
    
    MTKMesh = ObjCClass('MTKMesh')
    
    self.meshes = MTKMesh.newMeshesFromAsset_device_sourceMeshes_error_(asset, self.device, err_ptr, err_ptr)
    
    #pdbg.state(self.meshes.firstObject())
    #f = self.meshes.firstObject()
    
    #pdbg.state(f.vertexBuffers().objectAtIndexedSubscript_(0))
    
    #b = f.vertexBuffers().objectAtIndexedSubscript_(0)
    #pdbg.state(b.buffer())
    #mesh = self.meshes.firstObject()
    
    #pdbg.state(mesh.submeshes().firstObject())
    #submesh = mesh.submeshes().firstObject()
    #pdbg.state(submesh.indexBuffer().buffer())
    
    
    
    
  def renderer_init(self):
    def mtkView_drawableSizeWillChange_(_self, _cmd, _view, _size):
      pass
      
    def drawInMTKView_(_self, _cmd, _view):
      #view = ObjCInstance(_view)
      #drawable = self.view.currentDrawable()
      #descriptor = self.view.currentRenderPassDescriptor()
      
      view = ObjCInstance(_view)
      drawable = view.currentDrawable()
      descriptor = view.currentRenderPassDescriptor()
      pdbg.state(descriptor)
      
      
      #descriptor.colorAttachments().objectAtIndexedSubscript(0).texture = drawable.texture()
      #descriptor.colorAttachments().objectAtIndexedSubscript(0).setTexture_(view.currentDrawable().texture())
      descriptor.colorAttachments().objectAtIndexedSubscript(0).loadAction = 2  # .clear
      descriptor.colorAttachments().objectAtIndexedSubscript(0).clearColor = (0.5, 0.5, 0.5, 1)
      
      commandBuffer = self.commandQueue.commandBuffer()
      
      commandEncoder = commandBuffer.renderCommandEncoderWithDescriptor_(descriptor)
      
      commandEncoder.setRenderPipelineState_(self.renderPipelineState)
      commandEncoder.setDepthStencilState_(self.depthStencilState)
      commandEncoder.setCullMode_(2)  # .back
      commandEncoder.setFrontFacingWinding_(1)  # .counterClockwise
      
      commandEncoder.setVertexBuffer_offset_atIndex_(self.uniformsBuffer, 0, 0)
      
      commandEncoder.setFragmentTexture_atIndex_(self.texture)
      
      # --- step 4: set up Metal rendering and drawing of meshes
      
      mesh = self.meshes.firstObject()
      vertexBuffer = math.vertexBuffers().objectAtIndexedSubscript_(0)
      
      commandEncoder.setVertexBuffer_offset_atIndex_(vertexBuffer.buffer(), vertexBuffer.offset(), 0)
      
      submesh = mesh.submeshes().firstObject()
      
      commandEncoder.drawIndexedPrimitives_indexCount_indexType_indexBuffer_indexBufferOffset_(submesh.primitiveType(), submesh.indexCount(), submesh.indexType(), submesh.indexBuffer().buffer(), submesh.indexBuffer().offset())
      
      commandEncoder.endEncoding()
      commandBuffer.presentDrawable_(drawable)
      commandBuffer.commit()
      

    PyRenderer = create_objc_class(
      name='PyRenderer',
      methods=[drawInMTKView_, mtkView_drawableSizeWillChange_],
      protocols=['MTKViewDelegate'])
    return PyRenderer.new()
    


class MTKView(ui.View):
  # xxx: frame size
  def __init__(self, *args, **kwargs):
    ui.View.__init__(self, *args, **kwargs)
    self.bg_color = 'slategra'
    
    device = ObjCInstance(MTLCreateSystemDefaultDevice())

    _frame = ((0.0, 0.0), (300.0, 600.0))
    self.mtkView = ObjCClass('MTKView').alloc()
    
    #initWithFrame_device_
    #self.mtkView.initWithFrame_(_frame)
    self.mtkView.initWithFrame_device_(_frame, device)
    renderer = Renderer(self.mtkView).renderer_init()
    self.mtkView.delegate = renderer
    self.objc_instance.addSubview_(self.mtkView)
    


if __name__ == '__main__':
  view = MTKView()
  view.present(style='fullscreen', orientations=['portrait'])

