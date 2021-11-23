from math import radians
import ctypes

from .mScene import Scene
from .plane import Plane
from .cube import Cube
from .model import Model
from .structures import float3, float4


class LandscapeScene(Scene):
  def __init__(self, device, size):
    self.sun = Model(device, 'sun')
    super().__init__(device, size)
    self.add_childNode_(self.sun)
    self.sun.materialColor = float4(1.0, 1.0, 0.0, 1.0)
    
  def update_deltaTime_(self, deltaTime):
    # todo: 親の`Scene` が`pass` だけどとりあえず
    super().update_deltaTime_(deltaTime)

