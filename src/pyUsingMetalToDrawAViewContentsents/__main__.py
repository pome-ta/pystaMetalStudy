import ctypes
from objc_util import c, create_objc_class, ObjCClass, ObjCInstance, on_main_thread
import ui
import pdbg


MTKView = ObjCClass('MTKView')


MTLCreateSystemDefaultDevice = c.MTLCreateSystemDefaultDevice

MTLCreateSystemDefaultDevice.argtypes = []
MTLCreateSystemDefaultDevice.restype = ctypes.c_void_p

def initWithMetalKitView_(_self, _cmd, _mtkView):
  print('きた')
  self = ObjCInstance(_self)#.init()
  self.init()
  mtkView = ObjCInstance(_mtkView)
  self.device = mtkView.device()
  self.commandQueue = self.device.newCommandQueue()
  #return self.init()
  

def drawInMTKView_(_self, _cmd, _view):
  print('draw')
  self = ObjCInstance(_self)
  view = ObjCInstance(_view)
  renderPassDescriptor = view.currentRenderPassDescriptor()
  commandBuffer = self.commandQueue.commandBuffer()
  commandEncoder = commandBuffer.renderCommandEncoderWithDescriptor_(renderPassDescriptor)
  commandEncoder.endEncoding()
  drawable = view.currentDrawable()
  commandBuffer.presentDrawable_(drawable)
  commandBuffer.commit()
  

def mtkView_drawableSizeWillChange_(_self, _cmd, _view, _size):
  print('mtkView_drawableSizeWillChange_')
  
#mtkView_drawableSizeWillChange_.encoding = 'v@:@{CGSize}'
AAPLRenderer = create_objc_class(
  name='AAPLRenderer',
  methods=[initWithMetalKitView_, drawInMTKView_, mtkView_drawableSizeWillChange_],
  protocols=['MTKViewDelegate'])


class View(ui.View):
  def __init__(self, *args, **kwargs):
    ui.View.__init__(self, *args, **kwargs)
    self.instance = ObjCInstance(self)
    self.bg_color = 'maroon'
    self.view_did_load()

  #@on_main_thread
  def view_did_load(self):
    _view = MTKView.alloc()
    _view.enableSetNeedsDisplay = True
    _view.initWithFrame_device_(((0, 0), (256, 256)), ObjCInstance(MTLCreateSystemDefaultDevice()))
    _view.clearColor = (0.0, 0.5, 1.0, 1.0)
    
    _renderer = AAPLRenderer.alloc().initWithMetalKitView_(_view)
    _size = (_view.drawableSize().height, _view.drawableSize().width)
    _renderer.mtkView_drawableSizeWillChange_(_view, _size)
    #pdbg.state(_view.drawableSize().height)
    
    _view.delegate = _renderer
    
    
    #pdbg.state()

    self.instance.addSubview_(_view)


if __name__ == '__main__':
  view = View()
  view.present(style='fullscreen', orientations=['portrait'])

