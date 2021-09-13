from .metalNode import Node
from .matrixMath import matrix_float4x4


class Scene(Node):
  def __init__(self, device, size):
    super().__init__()
    self.device = device
    self.size = size
    
  def update_deltaTime_(self, deltaTime):
    print('scene')
    #print(dir(self))
    print(self.name)
    
    
  def render_commandEncoder_deltaTime_(self, commandEncoder, deltaTime):
    self.update_deltaTime_(deltaTime)
    #super().update_deltaTime_(deltaTime)
    #print(dir(self))
    #print(self.position)
    #print(self.name)
    viewMatrix = matrix_float4x4.translation_x_y_z_(
      0.0, 0.0, -14.0)
    for child in self.children:
      child.render_commandEncoder_parentModelViewMatrix_(
        commandEncoder, viewMatrix)
    

