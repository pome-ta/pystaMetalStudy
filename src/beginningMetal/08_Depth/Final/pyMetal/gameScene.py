from .metalScene import Scene
from .plane import Plane


class GameScene(Scene):
  def __init__(self, device, size):
    super().__init__(device, size)
    self.quad = Plane(device, 'picture.png')
    self.add_childNode_(self.quad)

