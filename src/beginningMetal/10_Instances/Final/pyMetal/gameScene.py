from math import radians
import ctypes

from .mScene import Scene
from .plane import Plane
from .cube import Cube
from .model import Model
from .structures import float3


class GameScene(Scene):
  def __init__(self, device, size):
    self.mushroom = Model(device, 'mushroom')

    super().__init__(device, size)
    self.add_childNode_(self.mushroom)

    self.camera.position.z = -6.0

  def update_deltaTime_(self, deltaTime):
    # todo: 親の`Scene` が`pass` だけどとりあえず
    super().update_deltaTime_(deltaTime)
    self.mushroom.rotation.y += deltaTime

