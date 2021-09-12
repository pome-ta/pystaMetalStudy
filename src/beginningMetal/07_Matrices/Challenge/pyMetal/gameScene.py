import ctypes

from .metalScene import Scene
from .plane import Plane

class float3(ctypes.Structure):
  _fields_ = [
    ('x', ctypes.c_float),
    ('y', ctypes.c_float),
    ('z', ctypes.c_float)
  ]


class GameScene(Scene):
  def __init__(self, device, size):
    super().__init__(device, size)
    self.quad = Plane(device, 'picture.png')
    self.quad.position.x = -1.0
    self.quad.position.y = 1.0
    self.add_childNode_(self.quad)
    '''
    self.quad2 = Plane(device, 'picture.png')
    self.quad2.scale = float3(0.5, 0.5, 0.5)
    self.quad2.position.y = 1.5
    self.add_childNode_(self.quad2)
    '''
    
  def update_deltaTime_(self, deltaTime):
    self.quad.rotation.y += deltaTime
    
    

