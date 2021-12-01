import ctypes

from objc_util import c, ObjCClass, ObjCInstance

# from .gameScene import GameScene
# from .landscapeScene import LandscapeScene
# from .instanceScene import InstanceScene
from .lightingScene import LightingScene
from .renderer import Renderer

import pdbg

wenderlichGreen = (0.0, 0.4, 0.21, 1.0)
skyBlue = (0.66, 0.9, 0.96, 1.0)


class MetalView:
  def __init__(self, bounds):
    self.devices = self.__createSystemDefaultDevice()
    self.mtkView = ObjCClass('MTKView').alloc()
    self.scene: 'Scene'
    self.view_did_load(bounds)
  
  def __createSystemDefaultDevice(self):
    MTLCreateSystemDefaultDevice = c.MTLCreateSystemDefaultDevice
    MTLCreateSystemDefaultDevice.argtypes = []
    MTLCreateSystemDefaultDevice.restype = ctypes.c_void_p
    return ObjCInstance(MTLCreateSystemDefaultDevice())
  
  def view_did_load(self, bounds):
    # xxx: `bounds` 全部入れる？
    _frame = ((0.0, 0.0), (bounds[2], bounds[3]))
    self.mtkView.initWithFrame_device_(_frame, self.devices).autorelease()
    self.mtkView.setAutoresizingMask_((1 << 1) | (1 << 4))
    self.mtkView.clearColor = wenderlichGreen
    self.scene = LightingScene(self.devices, bounds)
    self.scene.name = 'Lighting Scene'
    self.renderer = Renderer(self.devices).renderer_init(self.scene)
    self.mtkView.delegate = self.renderer
    
  def touch_began(self, touch):
    # xxx: `Renderer` からは、呼べない
    self.scene.touchesBegan_touches_(touch)
    
  def touch_moved(self, touch):
    self.scene.touchesMoved_touches_(touch)
    
