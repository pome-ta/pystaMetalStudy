import ctypes
from objc_util import c, ObjCClass, ObjCInstance
import ui

#import pdbg

# --- load objc classes
MTKView = ObjCClass('MTKView')

# --- initialize MetalDevice
MTLCreateSystemDefaultDevice = c.MTLCreateSystemDefaultDevice
MTLCreateSystemDefaultDevice.argtypes = []
MTLCreateSystemDefaultDevice.restype = ctypes.c_void_p


class View(ui.View):
  def __init__(self, *args, **kwargs):
    ui.View.__init__(self, *args, **kwargs)
    self.bg_color = 'maroon'
    self.view_did_load()

  def view_did_load(self):
    mtkView = MTKView.alloc()
    _device = MTLCreateSystemDefaultDevice()

    devices = ObjCInstance(_device)
    mtkView.initWithFrame_device_(((0, 0), (100, 100)), devices)
    mtkView.setAutoresizingMask_((1 << 1) | (1 << 4))

    self.objc_instance.addSubview_(mtkView)


if __name__ == '__main__':
  view = View()
  view.present(style='fullscreen', orientations=['portrait'])

