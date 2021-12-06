import ctypes

from objc_util import c, ObjCClass, ObjCInstance

from renderer import Renderer

import pdbg

clearColor = (0.0, 0.4, 0.21, 1.0)


class GameViewController:
  def __init__(self):
    self.view: MTKView
    self.renderer: Renderer

    self.viewDidLoad()

  def viewDidLoad(self):
    self.view = ObjCClass('MTKView').alloc()
    _frame = ((0.0, 0.0), (100, 100))
    self.view.initWithFrame_(_frame)
    # todo: frame size
    self.view.setAutoresizingMask_((1 << 1) | (1 << 4))
    self.view.device = self.__create_system_default_device()
    self.view.backgroundColor = clearColor
    
    self.renderer = Renderer()
    self.renderer.initWithMetalKitView_(self.view)

    #pdbg.state(self.view)

  def __create_system_default_device(self):
    MTLCreateSystemDefaultDevice = c.MTLCreateSystemDefaultDevice
    MTLCreateSystemDefaultDevice.argtypes = []
    MTLCreateSystemDefaultDevice.restype = ctypes.c_void_p
    return ObjCInstance(MTLCreateSystemDefaultDevice())


if __name__ == '__main__':
  GameViewController()
