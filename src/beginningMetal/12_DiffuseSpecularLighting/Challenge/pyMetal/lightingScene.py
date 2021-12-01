from .mScene import Scene
from .model import Model
from .structures import Float3


class LightingScene(Scene):
  def __init__(self, device, size):
    self.mushroom = Model(device, 'mushroom')
    self.previousTouchLocation = (0.0, 0.0)
    
    super().__init__(device, size)
    self.mushroom.specularIntensity = 0.2
    self.mushroom.shininess = 2.0
    self.mushroom.position.y = -1.0
    self.add_childNode_(self.mushroom)
    
    self.light.color = Float3(1.0, 1.0, 1.0)
    self.light.ambientIntensity = 0.2
    self.light.diffuseIntensity = 0.8
    self.light.direction = Float3(0.0, 0.0, -1.0)
  
  def update_deltaTime_(self, deltaTime):
    # todo: 親の`Scene` が`pass` だけどとりあえず
    super().update_deltaTime_(deltaTime)
    
  def touchesBegan_touches_(self, touches):
    super().touchesBegan_touches_(touches)
    self.previousTouchLocation = touches.location
    
  def touchesMoved_touches_(self, touches):
    super().touchesMoved_touches_(touches)
    touchLocation = touches.location
    delta_x = self.previousTouchLocation.x - touchLocation.x
    delta_y = self.previousTouchLocation.y - touchLocation.y
    sensitivity = 0.01
    self.mushroom.rotation.x += delta_y * sensitivity
    self.mushroom.rotation.y += delta_x * sensitivity
    self.previousTouchLocation = touchLocation
    
    
    
