import pathlib
import ctypes
from objc_util import c, create_objc_class, ObjCClass, ObjCInstance
import ui
import pdbg

shader_path = pathlib.Path('./pyShaders.metal')

# --- load objc classes
MTKView = ObjCClass('MTKView')
MTLRenderPipelineDescriptor = ObjCClass('MTLRenderPipelineDescriptor')
MTLCompileOptions = ObjCClass('MTLCompileOptions')

# --- initialize MetalDevice
MTLCreateSystemDefaultDevice = c.MTLCreateSystemDefaultDevice

MTLCreateSystemDefaultDevice.argtypes = []
MTLCreateSystemDefaultDevice.restype = ctypes.c_void_p

err_ptr = ctypes.c_void_p()


# --- set Structures
class Position(ctypes.Structure):
  _fields_ = [('x', ctypes.c_float), ('y', ctypes.c_float),
              ('z', ctypes.c_float), ('w', ctypes.c_float)]


class Color(ctypes.Structure):
  _fields_ = [('r', ctypes.c_float), ('g', ctypes.c_float),
              ('b', ctypes.c_float), ('a', ctypes.c_float)]


class Vertex(ctypes.Structure):
  _fields_ = [('position', Position), ('color', Color)]


class PyVertex(ctypes.Structure):
  _fields_ = [('x', Vertex), ('y', Vertex), ('z', Vertex)]


dataSize = 24 * 16

vertexData = PyVertex(
  Vertex(Position(-0.8, -0.8, 0.0, 1.0), Color(1.0, 0.0, 0.0, 1.0)),
  Vertex(Position(0.8, -0.8, 0.0, 1.0), Color(0.0, 1.0, 0.0, 1.0)),
  Vertex(Position(0.0, 0.8, 0.0, 1.0), Color(0.0, 0.0, 1.0, 1.0)))


# --- MTKViewDelegate
def drawInMTKView_(_self, _cmd, _view):
  self = ObjCInstance(_self)
  view = ObjCInstance(_view)
  commandBuffer = self.commandQueue.commandBuffer()
  renderPassDescriptor = view.currentRenderPassDescriptor()
  renderPassDescriptor.colorAttachments().objectAtIndexedSubscript(
    0).clearColor = (0.8, 0.4, 0.2, 1.0)

  renderEncoder = commandBuffer.renderCommandEncoderWithDescriptor_(renderPassDescriptor)

  renderEncoder.setRenderPipelineState_(self.pipelineState)
  renderEncoder.setVertexBuffer_offset_atIndex_(self.vertexBuffer, 0, 0)
  renderEncoder.drawPrimitives_vertexStart_vertexCount_instanceCount_(3, 0, 3, 1)
  renderEncoder.endEncoding()
  commandBuffer.presentDrawable_(view.currentDrawable())
  commandBuffer.commit()


def mtkView_drawableSizeWillChange_(_self, _cmd, _view, _size):
  #print('drawableSizeWillChange')
  pass


PyRenderer = create_objc_class(
  name='PyRenderer',
  methods=[drawInMTKView_, mtkView_drawableSizeWillChange_],
  protocols=['MTKViewDelegate'])


class View(ui.View):
  def __init__(self, *args, **kwargs):
    ui.View.__init__(self, *args, **kwargs)
    self.bg_color = 'maroon'

    self.view_did_load()

  def view_did_load(self):
    mtkView = MTKView.alloc()
    _device = MTLCreateSystemDefaultDevice()
    defaultDevice = ObjCInstance(_device)
    mtkView.initWithFrame_device_(((0, 0), (100, 100)), defaultDevice)
    mtkView.setAutoresizingMask_((1 << 1) | (1 << 4))

    renderer = self.renderer_init(PyRenderer, mtkView)
    mtkView.delegate = renderer

    self.objc_instance.addSubview_(mtkView)

  def renderer_init(self, delegate, _mtkView):
    source = shader_path.read_text('utf-8')
    renderer = delegate.alloc().init()
    renderer.device = _mtkView.device()

    renderer.commandQueue = renderer.device.newCommandQueue()

    library = renderer.device.newLibraryWithSource_options_error_(source, MTLCompileOptions.new(), err_ptr)

    vertexProgram = library.newFunctionWithName_('vertex_func')

    fragmentProgram = library.newFunctionWithName_('fragment_func')

    pipelineDescriptor = MTLRenderPipelineDescriptor.alloc().init()

    pipelineDescriptor.vertexFunction = vertexProgram
    pipelineDescriptor.fragmentFunction = fragmentProgram

    vertexBuffer = renderer.device.newBufferWithBytes_length_options_(ctypes.byref(vertexData), dataSize, 0)

    pipelineDescriptor.colorAttachments().objectAtIndexedSubscript(0).pixelFormat = 80

    pipelineState = renderer.device.newRenderPipelineStateWithDescriptor_error_(pipelineDescriptor, err_ptr)

    renderer.pipelineState = pipelineState
    renderer.vertexBuffer = vertexBuffer

    return renderer


if __name__ == '__main__':
  view = View()
  view.present(style='fullscreen', orientations=['portrait'])

