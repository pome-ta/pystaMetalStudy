from math import radians

from .mNode import Node
from .matrixMath import MatrixFloat4x4


class Camera(Node):
  def __init__(self):
    super().__init__()
    self.name = 'camera'
    self.fovDegrees = 65
    self.aspect = 1.0
    self.nearZ = 0.1
    self.farZ = 100
  
  def __fovRadians(self):
    return radians(self.fovDegrees)
  
  def viewMatrix(self):
    return self.modelMatrix
  
  def projectionMatrix(self):
    fov = self.__fovRadians()
    
    projectionMatrix = MatrixFloat4x4.projection_fov_aspect_nearZ_farZ_(
      fov, self.aspect, self.nearZ, self.farZ)
    return projectionMatrix
