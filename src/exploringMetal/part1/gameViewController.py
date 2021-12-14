import ctypes
from objc_util import c, ObjCClass, ObjCInstance

from renderer import Renderer


class GameViewController:
  def __init__(self):
    self.mtkView = ObjCClass('MTKView').alloc()
    self.renderer: Renderer
    self.devices = self.__createSystemDefaultDevice()
    self.viewDidLoad()

  def viewDidLoad(self):
    _frame = ((0.0, 0.0), (100, 100))
    self.mtkView.initWithFrame_device_(_frame, self.devices)
    self.mtkView.setAutoresizingMask_((1 << 1) | (1 << 4))
    self.renderer = Renderer(self.mtkView)
    self.mtkView.delegate = self.renderer.renderer_init()

  def __createSystemDefaultDevice(self):
    MTLCreateSystemDefaultDevice = c.MTLCreateSystemDefaultDevice
    MTLCreateSystemDefaultDevice.argtypes = []
    MTLCreateSystemDefaultDevice.restype = ctypes.c_void_p
    return ObjCInstance(MTLCreateSystemDefaultDevice())


if __name__ == '__main__':
  GameViewController()

