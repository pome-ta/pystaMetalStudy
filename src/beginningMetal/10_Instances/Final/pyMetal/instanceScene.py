from .mScene import Scene
from .instance import Instance


class InstanceScene(Scene):
  def __init__(self, device, size):
    humans = Instance(device, 'humanFigure', 40)
    super().__init__(device, size)
    self.add_childNode_(humans)

  def update_deltaTime_(self, deltaTime):
    # todo: 親の`Scene` が`pass` だけどとりあえず
    super().update_deltaTime_(deltaTime)

