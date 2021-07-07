from pathlib import Path
import ctypes
from objc_util import c, create_objc_class, ObjCClass, ObjCInstance
import ui
import pdbg

#shader_path = Path('./AAPLShaders.metal')
shader_path = Path('./Shaders.metal')
#shader_path = Path('./mShaders.metal')

# todo: load objc classes
MTKView = ObjCClass('MTKView')
MTLCompileOptions = ObjCClass('MTLCompileOptions')
MTLRenderPipelineDescriptor = ObjCClass('MTLRenderPipelineDescriptor')



err_ptr = ctypes.c_void_p()

MTLCreateSystemDefaultDevice = c.MTLCreateSystemDefaultDevice

MTLCreateSystemDefaultDevice.argtypes = []
MTLCreateSystemDefaultDevice.restype = ctypes.c_void_p

MTLPrimitiveTypeTriangle = 3


def drawInMTKView_(_self, _cmd, _view):
  self = ObjCInstance(_self)
  view = ObjCInstance(_view)

  commandBuffer = self.commandQueue.commandBuffer()
  commandBuffer.label = 'MyCommand'

  renderPassDescriptor = view.currentRenderPassDescriptor()

  if renderPassDescriptor != None:
    renderEncoder = commandBuffer.renderCommandEncoderWithDescriptor_(
      renderPassDescriptor)
    
    renderEncoder.label = 'MyRenderEncoder'
    #renderEncoder.drawPrimitives_vertexStart_vertexCount_(MTLPrimitiveTypeTriangle, 0, 3)
    renderEncoder.endEncoding()
    commandBuffer.presentDrawable_(view.currentDrawable())
  
  
  commandBuffer.commit()


def mtkView_drawableSizeWillChange_(_self, _cmd, _view, _size):
  print('mtkView_drawableSizeWillChange_')


AAPLRenderer = create_objc_class(
  name='AAPLRenderer',
  methods=[drawInMTKView_, mtkView_drawableSizeWillChange_],
  protocols=['MTKViewDelegate'])


class View(ui.View):
  def __init__(self, *args, **kwargs):
    ui.View.__init__(self, *args, **kwargs)
    self.instance = ObjCInstance(self)
    self.bg_color = 'maroon'
    self.view_did_load()

  def view_did_load(self):
    _view = MTKView.alloc()
    _view.enableSetNeedsDisplay = True
    _view.initWithFrame_device_(((0, 0), (256, 256)),
                                ObjCInstance(MTLCreateSystemDefaultDevice()))
    #_view.setAutoresizingMask_((1 << 1) | (1 << 4))
    _view.clearColor = (0.0, 0.5, 1.0, 1.0)
    _renderer = self.renderer_init(AAPLRenderer, _view)
    _view.delegate = _renderer

    self.instance.addSubview_(_view)

  # initWithMetalKitView:
  def renderer_init(self, delegate_cls, mtkView):
    renderer = delegate_cls.alloc().init()
    renderer.device = mtkView.device()

    shader_sauce = shader_path.read_text('utf-8')
    defaultLibrary = mtkView.device().newLibraryWithSource_options_error_(
      shader_sauce, MTLCompileOptions.new(), err_ptr)

    pdbg.state(defaultLibrary)
    
    #vertexFunction = defaultLibrary.newFunctionWithName_('vertexShader')
    #fragmentProgram = defaultLibrary.newFunctionWithName_('fragmentShader')
    
    pipelineStateDescriptor = MTLRenderPipelineDescriptor.alloc().init()
    
    
    
    renderer.commandQueue = renderer.device.newCommandQueue()
    return renderer


if __name__ == '__main__':
  view = View()
  view.present(style='fullscreen', orientations=['portrait'])

