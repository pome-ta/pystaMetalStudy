import ctypes

from objc_util import c, ObjCClass, ObjCInstance
import ui

from .renderer import Renderer
from .gameScene import GameScene

wenderlichGreen = (0.0, 0.4, 0.21, 1.0)

class MetalView:
  def __init__(self, bounds):
    self.devices = self.createSystemDefaultDevice()
    self.mtkView = ObjCClass('MTKView').alloc()
    self.view_did_load(bounds)

  def createSystemDefaultDevice(self):
    MTLCreateSystemDefaultDevice = c.MTLCreateSystemDefaultDevice
    MTLCreateSystemDefaultDevice.argtypes = []
    MTLCreateSystemDefaultDevice.restype = ctypes.c_void_p
    return ObjCInstance(MTLCreateSystemDefaultDevice())

  def view_did_load(self, bounds):
    # xxx: `bounds` 直？
    _frame = ((0.0, 0.0), (bounds[2], bounds[3]))
    self.mtkView.initWithFrame_device_(_frame, self.devices)
    #self.mtkView.setAutoresizingMask_((1 << 1) | (1 << 4))
    self.mtkView.clearColor = wenderlichGreen
    scene = GameScene(self.devices, bounds)
    renderer = Renderer(self.devices).renderer_init(scene)
    self.mtkView.delegate = renderer
