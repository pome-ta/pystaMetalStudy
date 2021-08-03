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
Vertex = (((ctypes.c_float * 4) * 2) * 4)
vertex_array = [
  [[-1.0, -1.0, 0.0,  1.0], [1.0, 0.0, 0.0, 1.0]],
  [[ 1.0, -1.0, 0.0,  1.0], [0.0, 1.0, 0.0, 1.0]],
  [[ 1.0,  1.0, 0.0,  1.0], [0.0, 0.0, 1.0, 1.0]],
  [[-1.0,  1.0, 0.0,  1.0], [1.0, 1.0, 1.0, 1.0]]
]
np_vertex = np.array(vertex_array, dtype=np.float32)
vertexData = np_vertex.ctypes.data_as(ctypes.POINTER(Vertex)).contents


Index = (ctypes.c_int16 * 6)
index_array = [0, 1, 2, 2, 3, 0]
np_index = np.array(index_array, dtype=np.uint16)
indexData = np_index.ctypes.data_as(ctypes.POINTER(Index)).contents


Matrix = (ctypes.c_float * 16)
np_m = np.eye(4, dtype=np.float32)
_matrixData = np_m.ctypes.data_as(ctypes.POINTER(Matrix)).contents




def translationMatrix(matrix, position):
  matrix[12] = position[0]
  matrix[13] = position[1]
  matrix[14] = position[2]
  return matrix

def scalingMatrix(matrix, scale):
  matrix[0] = scale
  matrix[5] = scale
  matrix[10] = scale
  matrix[15] = 1.0
  return matrix

def rotationMatrix(matrix, rot):
  matrix[0] = np.cos(rot[1]) * np.cos(rot[2])
  matrix[4] = np.cos(rot[2]) * np.sin(rot[0]) * np.sin(rot[1]) - np.cos(rot[0]) * np.sin(rot[2])
  matrix[8] = np.cos(rot[0]) * np.cos(rot[2]) * np.sin(rot[1]) + np.sin(rot[0]) * np.sin(rot[2])
  matrix[1] = np.cos(rot[1]) * np.sin(rot[2])
  matrix[5] = np.cos(rot[0]) * np.cos(rot[2]) + np.sin(rot[0]) * np.sin(rot[1]) * np.sin(rot[2])
  matrix[9] = -np.cos(rot[2]) * np.sin(rot[0]) + np.cos(rot[0]) * np.sin(rot[1]) * np.sin(rot[2])
  matrix[2] = -np.sin(rot[1])
  matrix[6] = np.cos(rot[1]) * np.sin(rot[0])
  matrix[10] = np.cos(rot[0]) * np.cos(rot[1])
  matrix[15] = 1.0
  return matrix

def modelMatrix(matrix):
  
  matrix = rotationMatrix(matrix, [0.0, 0.0, 0.1])
  matrix = scalingMatrix(matrix, 0.25)
  matrix = translationMatrix(matrix, [0.0, 0.5, 0.0])

  return matrix

matrixData = modelMatrix(_matrixData)


class MetalView(ui.View):
  def __init__(self, *args, **kwargs):
    ui.View.__init__(self, *args, **kwargs)
    self.bg_color = 'maroon'
    self.view_did_load()

  def view_did_load(self):
    mtkView = MTKView.alloc()
    _device = MTLCreateSystemDefaultDevice()
    devices = ObjCInstance(_device)
    
    # todo: 端末サイズにて要調整
    _uw, _uh = ui.get_window_size()
    _w = min(_uw, _uh) * 0.96
    _x = (_uw - _w) / 2
    _y = _uh / 4
    _frame = ((_x, _y), (_w, _w))

    
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

    renderer.vertexBuffer = renderer.device.newBufferWithBytes_length_options_(vertexData, 16 * (4 * 2), 0)
    
    renderer.indexBuffer = renderer.device.newBufferWithBytes_length_options_(indexData, 16 * 6, 0)


    renderer.uniformBuffer = renderer.device.newBufferWithLength_options_(16*16, 0)
    bufferPointer = renderer.uniformBuffer.contents()
    memcpy(bufferPointer, matrixData, 16 * 16)


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
