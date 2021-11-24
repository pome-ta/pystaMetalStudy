from random import random, randrange

from .structures import Float3
from .model import Model
from .mScene import Scene


class CrowdScene(Scene):
  def __init__(self, device, size):
    self.humans = []
    #self.humans = Model(device, 'humanFigure')
    super().__init__(device, size)
    for _ in range(40):
      human = Model(device, 'humanFigure')
      self.humans.append(human)
      self.add_childNode_(human)
      s_num = randrange(5) / 10
      human.scale = Float3(s_num, s_num, s_num)
      human.position.x = float(randrange(5)) - 2.0
      human.position.y = float(randrange(5)) - 3.0
      r, g, b = [random(), random(), random()]
      human.materialColor = (r, g, b, 1.0)
  
  def update_deltaTime_(self, deltaTime):
    # todo: 親の`Scene` が`pass` だけどとりあえず
    super().update_deltaTime_(deltaTime)
