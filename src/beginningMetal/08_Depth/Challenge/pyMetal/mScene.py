from .mNode import Node
from .matrixMath import matrix_float4x4


class Scene(Node):
  def __init__(self, device, size):
    super().__init__()
    self.device = device
    self.size = size
    self.deltaTime = None

  def update_deltaTime_(self, deltaTime):
    pass

  def render_commandEncoder_deltaTime_(self, commandEncoder, deltaTime):
    self.update_deltaTime_(deltaTime)
    viewMatrix = matrix_float4x4.translation_x_y_z_(
      0.0, 0.0, -14.0)
    for child in self.children:
      child.render_commandEncoder_parentModelViewMatrix_(
        commandEncoder, viewMatrix)

