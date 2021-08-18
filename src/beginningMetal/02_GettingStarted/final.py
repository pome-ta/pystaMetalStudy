import ctypes

from objc_util import c, create_objc_class, ObjCClass, ObjCInstance
import ui

import pdbg

# --- load objc classes
MTKView = ObjCClass('MTKView')

# --- initialize MetalDevice
MTLCreateSystemDefaultDevice = c.MTLCreateSystemDefaultDevice
MTLCreateSystemDefaultDevice.argtypes = []
MTLCreateSystemDefaultDevice.restype = ctypes.c_void_p

wenderlichGreen = (0.0, 0.4, 0.21, 1.0)


class PyMetal(ui.View):
  def __init__(self, *args, **kwargs):
    ui.View.__init__(self, *args, **kwargs)
    self.bg_color = 'slategray'
    self.view_did_load()

  def view_did_load(self):
    _device = MTLCreateSystemDefaultDevice()
    _frame = ((0.0, 0.0), (100.0, 100.0))
    devices = ObjCInstance(_device)
    mtkView = MTKView.alloc()
    mtkView.initWithFrame_device_(_frame, devices)
    mtkView.setAutoresizingMask_((1 << 1) | (1 << 4))

    mtkView.clearColor = wenderlichGreen

    mtk_delegate = self.delegate_init(PyRenderer, mtkView)
    mtkView.delegate = mtk_delegate

    self.objc_instance.addSubview_(mtkView)

  def delegate_init(self, delegate_cls, mtk_view):
    renderer = delegate_cls.alloc().init()
    device = mtk_view.device()
    renderer.commandQueue = device.newCommandQueue()
    return renderer


# --- MTKViewDelegate
def mtkView_drawableSizeWillChange_(_self, _cmd, _view, _size):
  self = ObjCInstance(_self)
  view = ObjCInstance(_view)


def drawInMTKView_(_self, _cmd, _view):
  self = ObjCInstance(_self)
  view = ObjCInstance(_view)
  drawable = view.currentDrawable()
  rpd = view.currentRenderPassDescriptor()
  commandBuffer = self.commandQueue.commandBuffer()
  commandEncoder = commandBuffer.renderCommandEncoderWithDescriptor_(rpd)

  commandEncoder.endEncoding()
  commandBuffer.presentDrawable_(drawable)
  commandBuffer.commit()


PyRenderer = create_objc_class(
  name='PyRenderer',
  methods=[drawInMTKView_, mtkView_drawableSizeWillChange_],
  protocols=['MTKViewDelegate'])

if __name__ == '__main__':
  view = PyMetal()
  view.present(style='fullscreen', orientations=['portrait'])

