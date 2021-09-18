from math import radians
import ctypes

from .metalScene import Scene
from .plane import Plane
from .cube import Cube
from .structures import float3


class GameScene(Scene):
  def __init__(self, device, size):
    
    self.cube = Cube(device)
    self.quad = Plane(device, 'picture.png')

    super().__init__(device, size)
    self.add_childNode_(self.cube)
    self.add_childNode_(self.quad)
    
    #self.cube.scale = float3(0.64, 0.64, 0.64)
    self.cube.scale = float3(1.64, 1.64, 1.64)
    self.quad.position.z = -3.0
    self.quad.scale = float3(3.0, 3.0, 3.0)
    
    
    self.camera.position.y = -1.0
    self.camera.position.x = 1.0
    self.camera.position.z = 6.0
    self.camera.rotation.x = radians(-45.0)
    self.camera.rotation.y = radians(-45.0)

  def update_deltaTime_(self, deltaTime):
    # todo: 親の`Scene` が`pass` だけどとりあえず呼んでる
    super().update_deltaTime_(deltaTime)
    #self.cube.rotation.y += deltaTime
    self.camera.rotation.y += deltaTime
    #print(self.camera.rotation)

