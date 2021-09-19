from math import radians

from .metalNode import Node
from .matrixMath import matrix_float4x4


class Camera(Node):
  def __init__(self):
    super().__init__()
    self.fovDegrees = 65
    self.aspect = 1.0
    self.nearZ = 0.1
    self.farZ = 100

  def __fovRadians(self):
    return radians(self.fovDegrees)

  def viewMatrix(self):
    self.modelMatrix = self.get_modelMatrix()
    return self.modelMatrix

  def projectionMatrix(self):
    fov = self.__fovRadians()

    projectionMatrix = matrix_float4x4.projection_fov_aspect_nearZ_farZ_(
      fov, self.aspect, self.nearZ, self.farZ)
    return projectionMatrix

