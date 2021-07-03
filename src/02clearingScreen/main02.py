import pathlib
import ctypes
from objc_util import c, create_objc_class, ObjCClass, ObjCInstance, ns, on_main_thread
import ui
import pdbg


shader_path = pathlib.Path('./Shaders.metal')

MTKView = ObjCClass('MTKView')
MTLRenderPipelineDescriptor = ObjCClass('MTLRenderPipelineDescriptor')
MTLCompileOptions = ObjCClass('MTLCompileOptions')

MTLCreateSystemDefaultDevice = c.MTLCreateSystemDefaultDevice

MTLCreateSystemDefaultDevice.argtypes = []
MTLCreateSystemDefaultDevice.restype = ctypes.c_void_p

err_ptr = ctypes.c_void_p()




vertexData = [
   0.0,  1.0, 0.0,
  -1.0, -1.0, 0.0,
   1.0, -1.0, 0.0
 ]
 


def drawInMTKView_(_self, _cmd, _view):
  d_self = ObjCInstance(_self)
  commandBuffer = d_self.commandQueue.commandBuffer()

  view = ObjCInstance(_view)
  renderPassDescriptor = view.currentRenderPassDescriptor()
  renderPassDescriptor.colorAttachments().objectAtIndexedSubscript(
    0).clearColor = (0.0, 0.5, 1.0, 1.0)

  renderEncoder = commandBuffer.renderCommandEncoderWithDescriptor_(
    renderPassDescriptor)

  '''renderEncoder.setRenderPipelineState_(d_self.pipelineState)
  renderEncoder.setVertexBuffer_offset_atIndex_(d_self.vertexBuffer, 0, 0)
  renderEncoder.drawPrimitives_vertexStart_vertexCount_('triangle', 0, 3)'''
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
    _device = MTLCreateSystemDefaultDevice()
    self.defaultDevice = ObjCInstance(_device)
    self.set_renderer()
    self.view_did_load()
    self.instance.addSubview_(self.mtkView)

  def view_did_load(self):
    self.mtkView = MTKView.alloc()
    
    self.mtkView.initWithFrame_device_(((0, 0), (100, 100)), self.defaultDevice)
    self.mtkView.setAutoresizingMask_((1 << 1) | (1 << 4))
    renderer = PyRenderer.alloc().init()
    renderer.commandQueue = self.mtkView.device().newCommandQueue()
    
    #pipelineState, vertexBuffer = self.set_renderer()
    '''
    renderer.pipelineState = pipelineState
    renderer.vertexBuffer = vertexBuffer'''
    self.mtkView.setDelegate_(renderer)
    #pdbg.state(self.mtkView.colorPixelFormat())
    
    
  @on_main_thread
  def set_renderer(self):
    pipelineDescriptor = MTLRenderPipelineDescriptor.alloc().init()
    
    
    # xxx: size の取り方 - `float` だから16にしてる
    dataSize = len(vertexData) * 16
    vertexBuffer = self.defaultDevice.newBufferWithBytes_length_options_(ns(vertexData), dataSize, 0)
    
    source = shader_path.read_text('utf-8')
    
    library = self.defaultDevice.newLibraryWithSource_options_error_(source, MTLCompileOptions.new(), err_ptr)
    fragmentProgram = library.newFunctionWithName_('basic_fragment')
    vertexProgram = library.newFunctionWithName_('basic_vertex')
    
    
    
    #pipelineDescriptor.colorAttachments().objectAtIndexedSubscript(0).pixelFormat = self.mtkView.colorPixelFormat
    
    pipelineState = self.defaultDevice.newRenderPipelineStateWithDescriptor_error_(pipelineDescriptor, err_ptr)
    pdbg.state(pipelineDescriptor)
    #return pipelineState, vertexBuffer


if __name__ == '__main__':
  view = View()
  view.present(style='fullscreen', orientations=['portrait'])

