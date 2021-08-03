import pathlib
import ctypes
import numpy as np

from objc_util import c, create_objc_class, ObjCClass, ObjCInstance
import ui

#import pdbg



shader_path = pathlib.Path('./Shaders.metal')


# --- load objc classes
MTKView = ObjCClass('MTKView')
MTLCompileOptions = ObjCClass('MTLCompileOptions')
MTLRenderPipelineDescriptor = ObjCClass('MTLRenderPipelineDescriptor')

# --- initialize MetalDevice
MTLCreateSystemDefaultDevice = c.MTLCreateSystemDefaultDevice
MTLCreateSystemDefaultDevice.argtypes = []
MTLCreateSystemDefaultDevice.restype = ctypes.c_void_p

memcpy = c.memcpy
memcpy.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t]
memcpy.restype = ctypes.c_void_p

err_ptr = ctypes.c_void_p()


# --- set Vertex
vertex_array = [
  [[-1.0, -1.0,  1.0, 1.0], [1.0, 0.0, 0.0, 1.0]],
  [[ 1.0, -1.0,  1.0, 1.0], [0.0, 1.0, 0.0, 1.0]],
  [[ 1.0,  1.0,  1.0, 1.0], [0.0, 0.0, 1.0, 1.0]],
  [[-1.0,  1.0,  1.0, 1.0], [1.0, 1.0, 1.0, 1.0]],
  [[-1.0, -1.0, -1.0, 1.0], [0.0, 0.0, 1.0, 1.0]],
  [[ 1.0, -1.0, -1.0, 1.0], [1.0, 1.0, 1.0, 1.0]],
  [[ 1.0,  1.0, -1.0, 1.0], [1.0, 0.0, 0.0, 1.0]],
  [[-1.0,  1.0, -1.0, 1.0], [0.0, 1.0, 0.0, 1.0]],
]
Vertex = (((ctypes.c_float * 4) * 2) * 8)
np_vertex = np.array(vertex_array, dtype=np.float32)


index_array = [
  0, 1, 2, 2, 3, 0,  # front
  1, 5, 6, 6, 2, 1,  # right
  3, 2, 6, 6, 7, 3,  # top
  4, 5, 1, 1, 0, 4,  # bottom
  4, 0, 3, 3, 7, 4,  # left
  7, 6, 5, 5, 4, 7,  # back
]
Index = (ctypes.c_uint16 * 36)
np_index = np.array(index_array, dtype=np.uint16)

#MatrixFloat4x4 = ((ctypes.c_float * 4) *4)
MatrixFloat4x4 = (ctypes.c_float *16)


class Uniforms(ctypes.Structure):
  _fields_ = [('modelViewProjectionMatrix', MatrixFloat4x4)]


# --- Matrix func
def translationMatrix(position):
  _matrix4x4 = np.identity(4, dtype=np.float32)
  _matrix4x4[3] = [position[0], position[1], position[2], 1.0]
  
  return _matrix4x4

def scalingMatrix(scale):
  _matrix4x4 = np.identity(4, dtype=np.float32)
  _matrix4x4[0, 0] = scale
  _matrix4x4[1, 1] = scale
  _matrix4x4[2, 2] = scale
  _matrix4x4[3, 3] = 1.0
  
  return _matrix4x4
  
def rotationMatrix(angle, axis):
  X = np.zeros(4, dtype=np.float32)
  X[0] = axis[0] * axis[0] + (1.0 - axis[0] * axis[0]) * np.cos(angle)
  X[1] = axis[0] * axis[1] * (1.0 - np.cos(angle)) - axis[2] * np.sin(angle)
  X[2] = axis[0] * axis[2] * (1.0 - np.cos(angle)) + axis[1] * np.sin(angle)
  X[3] = 0.0
  
  Y = np.zeros(4, dtype=np.float32)
  Y[0] = axis[0] * axis[1] * (1.0 - np.cos(angle))  + axis[2] * np.sin(angle)
  Y[1] = axis[1] * axis[1] + (1.0 - axis[1] * axis[1]) * np.cos(angle)
  Y[2] = axis[1] * axis[2] * (1.0 - np.cos(angle)) - axis[0] * np.sin(angle)
  Y[3] = 0.0
  
  Z = np.zeros(4, dtype=np.float32)
  Z[0] = axis[0] * axis[2] * (1.0 - np.cos(angle)) - axis[1] * np.sin(angle)
  Z[1] = axis[1] * axis[2] * (1.0 - np.cos(angle)) + axis[0] * np.sin(angle)
  Z[2] = axis[2] * axis[2] + (1.0 - axis[2] * axis[2]) * np.cos(angle)
  Z[3] = 0.0
  
  W = np.zeros(4, dtype=np.float32)
  W[3] = 1.0
  
  _matrix4x4 = np.vstack((X, Y, Z, W))
  
  return _matrix4x4


def projectionMatrix(near, far, aspect, fovy):
  scaleY = 1.0 / np.tan(fovy * 0.5)
  scaleX = scaleY / aspect
  scaleZ = -(far + near) / (far - near)
  scaleW = -2.0 * far * near / (far - near)
  X = np.array([scaleX, 0.0, 0.0, 0.0], dtype=np.float32)
  Y = np.array([0.0, scaleY, 0.0, 0.0], dtype=np.float32)
  Z = np.array([0.0, 0.0, scaleZ, -1.0], dtype=np.float32)
  W = np.array([0.0, 0.0, scaleW, 0.0], dtype=np.float32)
  
  _matrix4x4 = np.vstack((X, Y, Z, W))
  
  return _matrix4x4
  



# todo: 無駄にキャストするテスト
__vertexData = np_vertex.ctypes.data_as(ctypes.POINTER(Vertex)).contents
_vertexData = np.ctypeslib.as_array(__vertexData)
vertexData = _vertexData.ctypes.data_as(ctypes.POINTER(Vertex)).contents


indexData = np_index.ctypes.data_as(ctypes.POINTER(Index)).contents



class MetalView(ui.View):
  def __init__(self, *args, **kwargs):
    ui.View.__init__(self, *args, **kwargs)
    self.bg_color = 'maroon'
    self.view_did_load()

  def view_did_load(self):
    mtkView = MTKView.alloc()
    _device = MTLCreateSystemDefaultDevice()

    # todo: 端末サイズにて要調整
    _uw, _uh = ui.get_window_size()
    _w = min(_uw, _uh) * 0.96
    _x = (_uw - _w) / 2
    _y = _uh / 4

    #_frame = ((32.0, 32.0), (300.0, 300.0))
    #_frame = ((0.0, 0.0), (300.0, 300.0))
    _frame = ((_x, _y), (_w, _w))

    devices = ObjCInstance(_device)
    mtkView.initWithFrame_device_(_frame, devices)
    #mtkView.setAutoresizingMask_((1 << 1) | (1 << 4))
    renderer = self.renderer_init(PyRenderer, mtkView)
    mtkView.delegate = renderer
    self.objc_instance.addSubview_(mtkView)

  def renderer_init(self, delegate, _mtkView):
    renderer = delegate.alloc().init()

    # --- createBuffer
    renderer.device = _mtkView.device()
    renderer.commandQueue = renderer.device.newCommandQueue()

    # xxx: length
    renderer.vertexBuffer = renderer.device.newBufferWithBytes_length_options_(vertexData, np_vertex.nbytes, 0)
    renderer.indexBuffer = renderer.device.newBufferWithBytes_length_options_(indexData, np_index.nbytes, 0)
    print(np_index.nbytes)
    
    renderer.uniformBuffer = renderer.device.newBufferWithLength_options_(64, 0)
    bufferPointer = renderer.uniformBuffer.contents()
    
    renderer.rotation = 0.0
    

    # --- registerShaders
    source = shader_path.read_text('utf-8')
    library = renderer.device.newLibraryWithSource_options_error_(source, MTLCompileOptions.new(), err_ptr)

    vertex_func = library.newFunctionWithName_('vertex_func')
    frag_func = library.newFunctionWithName_('fragment_func')

    rpld = MTLRenderPipelineDescriptor.new()
    rpld.vertexFunction = vertex_func
    rpld.fragmentFunction = frag_func
    rpld.colorAttachments().objectAtIndexedSubscript(0).pixelFormat = 80  # .bgra8Unorm

    renderer.rps = renderer.device.newRenderPipelineStateWithDescriptor_error_(rpld, err_ptr)

    return renderer


# --- MTKViewDelegate
def drawInMTKView_(_self, _cmd, _view):
  self = ObjCInstance(_self)
  view = ObjCInstance(_view)
  # --- update
  scaled = scalingMatrix(0.5)
  self.rotation += 1 / 100 * np.pi / 4.0
  rotatedY = rotationMatrix(self.rotation, [0.0, 1.0, 0.0])
  rotatedX = rotationMatrix(np.pi / 4.0, [1.0, 0.0, 0.0])
  modelMatrix = np.dot(np.dot(rotatedX, rotatedY), scaled)
  cameraPosition = [0.0, 0.0, -3.0]
  viewMatrix = translationMatrix(cameraPosition)
  projMatrix = projectionMatrix(0.0, 10.0, 1.0, 1.0)
  # todo: ここで、`ctypes` へキャスト
  _modelViewProjectionMatrix = np.dot(projMatrix, np.dot(viewMatrix, modelMatrix))
  modelViewProjectionMatrix = _modelViewProjectionMatrix.ctypes.data_as(ctypes.POINTER(MatrixFloat4x4)).contents
  
  bufferPointer = self.uniformBuffer.contents()
  uniforms = Uniforms(modelViewProjectionMatrix)
  memcpy(bufferPointer, ctypes.byref(uniforms), 64)
  
  
  drawable = view.currentDrawable()
  rpd = view.currentRenderPassDescriptor()
  rpd.colorAttachments().objectAtIndexedSubscript(0).clearColor = (0.0, 0.5, 0.5, 1.0)

  commandBuffer = self.commandQueue.commandBuffer()
  commandEncoder = commandBuffer.renderCommandEncoderWithDescriptor_(rpd)
  commandEncoder.setRenderPipelineState_(self.rps)
  
  # MTLWinding
  #   clockwise = 0
  #   counterClockwise = 1
  # MTLCullMode
  #   none = 0
  #   front = 1
  #   back = 2
  commandEncoder.setFrontFacingWinding_(1)  # .counterClockwise
  commandEncoder.setCullMode_(2)  # .back
  commandEncoder.setVertexBuffer_offset_atIndex_(self.vertexBuffer, 0, 0)
  commandEncoder.setVertexBuffer_offset_atIndex_(self.uniformBuffer, 0, 1)

  commandEncoder.drawIndexedPrimitives_indexCount_indexType_indexBuffer_indexBufferOffset_(3, 36, 0, self.indexBuffer, 0)

  commandEncoder.endEncoding()
  commandBuffer.presentDrawable_(drawable)
  commandBuffer.commit()


def mtkView_drawableSizeWillChange_(_self, _cmd, _view, _size):
  self = ObjCInstance(_self)
  view = ObjCInstance(_view)


PyRenderer = create_objc_class(
  name='PyRenderer',
  methods=[drawInMTKView_, mtkView_drawableSizeWillChange_],
  protocols=['MTKViewDelegate'])

if __name__ == '__main__':
  view = MetalView()
  view.present(style='fullscreen', orientations=['portrait'])
