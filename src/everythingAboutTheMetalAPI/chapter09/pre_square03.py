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
Vertex = (((ctypes.c_float * 4) * 2) * 8)
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
np_vertex = np.array(vertex_array, dtype=np.float32)

Index = (ctypes.c_uint16 * 36)
index_array = [
  0, 1, 2, 2, 3, 0,  # front
  1, 5, 6, 6, 2, 1,  # right
  3, 2, 6, 6, 7, 3,  # top
  4, 5, 1, 1, 0, 4,  # bottom
  4, 0, 3, 3, 7, 4,  # left
  7, 6, 5, 5, 4, 7,  # back
]
np_index = np.array(index_array, dtype=np.uint16)

#MatrixFloat4x4 = ((ctypes.c_float * 4) *4)
MatrixFloat4x4 = (ctypes.c_float *16)


class Uniforms(ctypes.Structure):
  _fields_ = [('modelViewProjectionMatrix', MatrixFloat4x4)]


# --- Matrix func
def scalingMatrix(scale):
  _xyzw = np.identity(4, dtype=np.float32)
  _xyzw[0, 0] = scale
  _xyzw[1, 1] = scale
  _xyzw[2, 2] = scale
  
  return _xyzw
  
def rotationMatrix(angle, axis):
  x = np.zeros(4, dtype=np.float32)
  x[0] = axis[0] * axis[0] + (1.0 - axis[0] * axis[0]) * np.cos(angle)
  x[1] = axis[0] * axis[1] * (1.0 - np.cos(angle)) - axis[2] * np.sin(angle)
  x[2] = axis[0] * axis[2] * (1.0 - np.cos(angle)) + axis[1] * np.sin(angle)
  x[3] = 0.0
  
  y = np.zeros(4, dtype=np.float32)
  y[0] = axis[0] * axis[1] * (1.0 - np.cos(angle))  + axis[2] * np.sin(angle)
  y[1] = axis[1] * axis[1] + (1.0 - axis[1] * axis[1]) * np.cos(angle)
  y[2] = axis[1] * axis[2] * (1.0 - np.cos(angle)) - axis[0] * np.sin(angle)
  y[3] = 0.0
  
  z = np.zeros(4, dtype=np.float32)
  z[0] = axis[0] * axis[2] * (1.0 - np.cos(angle)) - axis[1] * np.sin(angle)
  z[1] = axis[1] * axis[2] * (1.0 - np.cos(angle)) + axis[0] * np.sin(angle)
  z[2] = axis[2] * axis[2] + (1.0 - axis[2] * axis[2]) * np.cos(angle)
  z[3] = 0.0
  
  w = np.zeros(4, dtype=np.float32)
  w[3] = 1.0
  
  #_xyzw = np.array([x, y, z, w], dtype=np.float32)
  _xyzw = np.vstack((x, y, z, w))
  
  return _xyzw


def matrixMultiply(a3x2, a3x3):
  return np.dot(a3x2[:2, :3], a3x3[:3, :3])
  
  

def modelMatrix():
  scaled = scalingMatrix(0.5)
  rotatedY = rotationMatrix(np.pi / 4, [0.0, 1.0, 0.0])
  rotatedX = rotationMatrix(np.pi / 4, [1.0, 0.0, 0.0])
  
  #_xy = matrixMultiply(rotatedX, rotatedY)
  _xy = rotatedX * rotatedY
  #_matrix = matrixMultiply(_xy, scaled)
  _matrix = _xy * scaled
  
  
  return _matrix


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
    renderer.indexBuffer = renderer.device.newBufferWithBytes_length_options_(indexData, np_index.nbytes * 8, 0)

    renderer.uniformBuffer = renderer.device.newBufferWithLength_options_(16 * 16, 0)
    bufferPointer = renderer.uniformBuffer.contents()
    
    # todo: ここで、`ctypes` へキャスト
    _modelViewProjectionMatrix = modelMatrix()
    modelViewProjectionMatrix = _modelViewProjectionMatrix.ctypes.data_as(ctypes.POINTER(MatrixFloat4x4)).contents
    
    uniforms = Uniforms(modelViewProjectionMatrix)
    
    memcpy(bufferPointer, ctypes.byref(uniforms), 16 * 16)

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

  drawable = view.currentDrawable()
  rpd = view.currentRenderPassDescriptor()
  rpd.colorAttachments().objectAtIndexedSubscript(0).clearColor = (0.0, 0.5, 0.5, 1.0)

  commandBuffer = self.commandQueue.commandBuffer()
  commandEncoder = commandBuffer.renderCommandEncoderWithDescriptor_(rpd)
  commandEncoder.setRenderPipelineState_(self.rps)
  commandEncoder.setVertexBuffer_offset_atIndex_(self.vertexBuffer, 0, 0)
  commandEncoder.setVertexBuffer_offset_atIndex_(self.uniformBuffer, 0, 1)

  commandEncoder.drawIndexedPrimitives_indexCount_indexType_indexBuffer_indexBufferOffset_(3, (self.indexBuffer.length() // 16), 0, self.indexBuffer, 0)

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
