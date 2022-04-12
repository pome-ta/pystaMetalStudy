from .mScene import Scene
from .model import Model
from .structures import Float3


class LightingScene(Scene):
  def __init__(self, device, size):
    self.mushroom = Model(device, 'mushroom')
    super().__init__(device, size)
    self.mushroom.position.y = -1.0
    self.add_childNode_(self.mushroom)
    
    self.light.color = Float3(0.0, 0.0, 1.0)
    self.light.ambientIntensity = 0.5
  
  def update_deltaTime_(self, deltaTime):
    # todo: 親の`Scene` が`pass` だけどとりあえず
    super().update_deltaTime_(deltaTime)
