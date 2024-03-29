import pathlib
import ctypes
from objc_util import c, create_objc_class, ObjCClass, ObjCInstance, ns
import ui
#import pdbg

shader_path = pathlib.Path('./Shaders.metal')

# --- load objc classes
MTKView = ObjCClass('MTKView')
MTLRenderPipelineDescriptor = ObjCClass('MTLRenderPipelineDescriptor')
MTLCompileOptions = ObjCClass('MTLCompileOptions')

# --- initialize MetalDevice
MTLCreateSystemDefaultDevice = c.MTLCreateSystemDefaultDevice

MTLCreateSystemDefaultDevice.argtypes = []
MTLCreateSystemDefaultDevice.restype = ctypes.c_void_p

err_ptr = ctypes.c_void_p()

float_3 = ctypes.c_float * 3


class Vertex(ctypes.Structure):
  _fields_ = [('ax', float_3), ('ay', float_3), ('az', float_3)]


vertexData = Vertex((0.0, 1.0, 0.0), (-1.0, -1.0, 0.0), (1.0, -1.0, 0.0))


def drawInMTKView_(_self, _cmd, _view):
  self = ObjCInstance(_self)
  view = ObjCInstance(_view)
  commandBuffer = self.commandQueue.commandBuffer()
  renderPassDescriptor = view.currentRenderPassDescriptor()
  renderPassDescriptor.colorAttachments().objectAtIndexedSubscript(
    0).setTexture_(view.currentDrawable().texture())
  renderPassDescriptor.colorAttachments().objectAtIndexedSubscript(
    0).clearColor = (1.0, 0.0, 0.0, 1.0)

  renderEncoder = commandBuffer.renderCommandEncoderWithDescriptor_(
    renderPassDescriptor)

  renderEncoder.setRenderPipelineState_(self.pipelineState)
  renderEncoder.setVertexBuffer_offset_atIndex_(self.vertexBuffer, 0, 0)
  renderEncoder.drawPrimitives_vertexStart_vertexCount_instanceCount_(
    3, 0, 3, 1)     
  renderEncoder.endEncoding()
  commandBuffer.presentDrawable_(view.currentDrawable())
  commandBuffer.commit()


def mtkView_drawableSizeWillChange_(_self, _cmd, _view, _size):
  print('drawableSizeWillChange')


PyRenderer = create_objc_class(
  name='PyRenderer',
  methods=[drawInMTKView_, mtkView_drawableSizeWillChange_],
  protocols=['MTKViewDelegate'])


class View(ui.View):
  def __init__(self, *args, **kwargs):
    ui.View.__init__(self, *args, **kwargs)
    self.bg_color = 'maroon'
    self.instance = ObjCInstance(self)

    self.view_did_load()
    self.instance.addSubview_(self.mtkView)

  def view_did_load(self):
    self.mtkView = MTKView.alloc()
    _device = MTLCreateSystemDefaultDevice()
    defaultDevice = ObjCInstance(_device)
    self.mtkView.initWithFrame_device_(((0, 0), (100, 100)), defaultDevice)
    self.mtkView.setAutoresizingMask_((1 << 1) | (1 << 4))
    renderer = PyRenderer.alloc().init()
    renderer.commandQueue = self.mtkView.device().newCommandQueue()

    pipelineDescriptor = MTLRenderPipelineDescriptor.alloc().init()

    # xxx: size の取り方 - `float` だから16にしてる
    dataSize = 9 * 16
    vertexBuffer = self.mtkView.device().newBufferWithBytes_length_options_(
      ctypes.byref(vertexData), dataSize, 0)

    source = shader_path.read_text('utf-8')

    library = self.mtkView.device().newLibraryWithSource_options_error_(
      source, MTLCompileOptions.new(), err_ptr)

    fragmentProgram = library.newFunctionWithName_('basic_fragment')
    vertexProgram = library.newFunctionWithName_('basic_vertex')

    pipelineDescriptor.vertexFunction = vertexProgram
    pipelineDescriptor.fragmentFunction = fragmentProgram

    pipelineDescriptor.colorAttachments().objectAtIndexedSubscript(
      0).pixelFormat = self.mtkView.colorPixelFormat()

    pipelineState = self.mtkView.device(
    ).newRenderPipelineStateWithDescriptor_error_(pipelineDescriptor, err_ptr)

    renderer.pipelineState = pipelineState
    renderer.vertexBuffer = vertexBuffer
    self.mtkView.setDelegate_(renderer)


if __name__ == '__main__':
  view = View()
  view.present(style='fullscreen', orientations=['portrait'])


