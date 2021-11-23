from .structures import Float3
from .instance import Instance
from .mScene import Scene


class InstanceScene(Scene):
  def __init__(self, device, size):
    self.humans = Instance(device, 'humanFigure', 40)
    super().__init__(device, size)
    self.add_childNode_(self.humans)
    
    for human in self.humans.nodes:
      human.scale = Float3(0.5, 0.5, 0.5)
      human.position.x = -2.0
      human.position.y = -3.0
      human.materialColor = (0.5, 0.0, 1.0, 1.0)
  
  def update_deltaTime_(self, deltaTime):
    # todo: 親の`Scene` が`pass` だけどとりあえず
    super().update_deltaTime_(deltaTime)
