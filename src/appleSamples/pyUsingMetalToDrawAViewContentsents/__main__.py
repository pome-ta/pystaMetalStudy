import ctypes
from objc_util import c, create_objc_class, ObjCClass, ObjCInstance
import ui
import pdbg

MTKView = ObjCClass('MTKView')

MTLCreateSystemDefaultDevice = c.MTLCreateSystemDefaultDevice

MTLCreateSystemDefaultDevice.argtypes = []
MTLCreateSystemDefaultDevice.restype = ctypes.c_void_p


def drawInMTKView_(_self, _cmd, _view):
  self = ObjCInstance(_self)
  view = ObjCInstance(_view)
  renderPassDescriptor = view.currentRenderPassDescriptor()
  commandBuffer = self.commandQueue.commandBuffer()
  commandEncoder = commandBuffer.renderCommandEncoderWithDescriptor_(
    renderPassDescriptor)
  commandEncoder.endEncoding()
  drawable = view.currentDrawable()
  commandBuffer.presentDrawable_(drawable)
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
    renderer.commandQueue = renderer.device.newCommandQueue()
    return renderer


if __name__ == '__main__':
  view = View()
  view.present(style='fullscreen', orientations=['portrait'])

