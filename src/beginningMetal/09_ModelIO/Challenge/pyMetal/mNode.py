import ctypes

from .matrixMath import matrix_float4x4, matrix_multiply
from .structures import float3, float4


class Node:
  def __init__(self):
    self.modelMatrix: 'matrix'
    self.name = 'Untitled'
    self.materialColor = float4(1.0, 1.0, 1.0, 1.0)
    self.children = []
    self.position = float3(0.0, 0.0, 0.0)
    self.rotation = float3(0.0, 0.0, 0.0)
    self.scale = float3(1.0, 1.0, 1.0)

  @property
  def modelMatrix(self):
    return self.__get_modelMatrix()
  
  def __get_modelMatrix(self):
    matrix = matrix_float4x4.translation_x_y_z_(
      self.position.x, self.position.y, self.position.z)
    matrix = matrix.rotatedBy_angle_x_y_z_(
      self.rotation.x, 1.0, 0.0, 0.0)
    matrix = matrix.rotatedBy_angle_x_y_z_(
      self.rotation.y, 0.0, 1.0, 0.0)
    matrix = matrix.rotatedBy_angle_x_y_z_(
      self.rotation.z, 0.0, 0.0, 1.0)
    matrix = matrix.scaledBy_x_y_z_(
      self.scale.x, self.scale.y, self.scale.z)
    return matrix

  def add_childNode_(self, childNode):
    self.children.append(childNode)

  def render_commandEncoder_parentModelViewMatrix_(self, commandEncoder, parentModelViewMatrix):
    modelViewMatrix = matrix_multiply(
      parentModelViewMatrix, self.modelMatrix)

    for child in self.children:
      print(child.name)
      child.render_commandEncoder_parentModelViewMatrix_(
        commandEncoder, modelViewMatrix)
    # xxx: `if let renderable = self as? Renderable` ?
    if 'doRender_commandEncoder_modelViewMatrix_' in dir(self):
      renderable = self
      renderable.doRender_commandEncoder_modelViewMatrix_(
        commandEncoder, modelViewMatrix)
