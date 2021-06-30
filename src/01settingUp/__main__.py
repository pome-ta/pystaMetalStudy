import pathlib
import ctypes
from objc_util import c, create_objc_class, load_framework, ObjCClass, ObjCInstance
import ui
import pdbg

# xxx: いる？
#load_framework('Metal')
#load_framework('MetalKit')

MTKView = ObjCClass('MTKView')

MTLCreateSystemDefaultDevice = c.MTLCreateSystemDefaultDevice

MTLCreateSystemDefaultDevice.argtypes = []
MTLCreateSystemDefaultDevice.restype = ctypes.c_void_p


def drawInMTKView_(_self, _cmd, view):
  #print('drawInMTKView')
  pass


def mtkView_drawableSizeWillChange_(_self, _cmd, view, size):
  #print('drawableSizeWillChange')
  pass


pyRenderer = create_objc_class(
  name='pyRenderer',
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
    self.mtkView.setDelegate_(pyRenderer.new())


if __name__ == '__main__':
  view = View()
  view.present(style='fullscreen', orientations=['portrait'])

