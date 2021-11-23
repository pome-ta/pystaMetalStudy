from random import random, randrange

from .structures import Float3
from .instance import Instance
from .mScene import Scene


class InstanceScene(Scene):
  def __init__(self, device, size):
    self.humans = Instance(device, 'humanFigure', 1)
    super().__init__(device, size)
    self.add_childNode_(self.humans)
    
    for human in self.humans.nodes:
      #s_num = randrange(5) / 10
      #human.scale = Float3(s_num, s_num, s_num)
      # xxx: 確認用
      human.scale = Float3(0.5, 0.5, 0.5)
      human.position.x = float(randrange(5)) - 2.0
      human.position.y = float(randrange(5)) - 3.0
      human.materialColor = (random(), random(), random(), 1.0)
  
  def update_deltaTime_(self, deltaTime):
    # todo: 親の`Scene` が`pass` だけどとりあえず
    super().update_deltaTime_(deltaTime)
