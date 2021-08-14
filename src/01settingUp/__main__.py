import pathlib
import ctypes

from objc_util import c, create_objc_class, load_framework, ObjCClass, ObjCInstance
import ui

import pdbg

MTKView = ObjCClass('MTKView')

MTLCreateSystemDefaultDevice = c.MTLCreateSystemDefaultDevice

MTLCreateSystemDefaultDevice.argtypes = []
MTLCreateSystemDefaultDevice.restype = ctypes.c_void_p


class View(ui.View):
  def __init__(self, *args, **kwargs):
    ui.View.__init__(self, *args, **kwargs)
    self.bg_color = 'maroon'
    self.view_did_load()

  def view_did_load(self):
    _device = MTLCreateSystemDefaultDevice()
    defaultDevice = ObjCInstance(_device)

    mtkView = MTKView.alloc()
    mtkView.initWithFrame_device_(((0, 0), (100, 100)), defaultDevice)
    mtkView.setAutoresizingMask_((1 << 1) | (1 << 4))

    renderer = self.renderer_init(pyRenderer, mtkView)
    mtkView.delegate = renderer

    self.objc_instance.addSubview_(mtkView)

  def renderer_init(self, delegate, _mtkView):
    renderer = delegate.alloc().init()
    return renderer


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

if __name__ == '__main__':
  view = View()
  view.present(style='fullscreen', orientations=['portrait'])

