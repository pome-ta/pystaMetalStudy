from math import radians
from random import choice, randrange

from .instance import Instance
from .mScene import Scene
from .model import Model
from .plane import Plane
from .structures import Float3, Float4


class LandscapeScene(Scene):
  def __init__(self, device, size):
    self.ground = Plane(device)
    self.grass = Instance(device, 'grass', 10000)
    self.mushroom = Model(device, 'mushroom')
    self.sun = Model(device, 'sun')
    super().__init__(device, size)
    self.add_childNode_(self.sun)
    self.sun.materialColor = Float4(1.0, 1.0, 0.0, 1.0)
    
    self.setupScene()
    

  def setupScene(self):
    self.ground.materialColor = Float4(0.4, 0.3, 0.1, 1.0)  # brown
    self.add_childNode_(self.ground)
    self.add_childNode_(self.grass)
    self.add_childNode_(self.mushroom)

    self.ground.scale = Float3(20.0, 20.0, 20.0)
    self.ground.rotation.x = radians(90.0)

    self.camera.rotation.x = radians(-10.0)
    self.camera.position.z = -20.0
    self.camera.position.y = -2

    greens = [
      Float4(0.34, 0.51, 0.01, 1.0),
      Float4(0.5, 0.5, 0.0, 1.0),
      Float4(0.29, 0.36, 0.14, 1.0)]
    
    for row in range(100):
      for column in range(100):
        position = Float3(0.0, 0.0, 0.0)
        position.x = float(row) / 4
        position.z = float(column) / 4
        
        blade = self.grass.nodes[row * 100 + column]
        blade.scale = Float3(0.5, 0.5, 0.5)
        blade.position = position
        
        blade.materialColor = choice(greens)
        blade.rotation.y = radians(float(randrange(360)))
    
    self.grass.position.x = -12.0
    self.grass.position.z = -12.0
    
    self.mushroom.position.x = -6.0
    self.mushroom.position.z = -8.0
    self.mushroom.scale = Float3(2.0,2.0,2.0)
    
    self.sun.position.y = 7.0
    self.sun.position.x = 6.0
    self.sun.scale = Float3(2.0, 2.0, 2.0)
    
    self.camera.fovDegrees = 25.0
    

  def update_deltaTime_(self, deltaTime):
    # todo: 親の`Scene` が`pass` だけどとりあえず
    super().update_deltaTime_(deltaTime)
