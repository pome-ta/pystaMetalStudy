import ctypes

from .matrixMath import matrix_float4x4, matrix_multiply


class float3(ctypes.Structure):
  _fields_ = [
    ('x', ctypes.c_float),
    ('y', ctypes.c_float),
    ('z', ctypes.c_float)
  ]

class Node:
  def __init__(self):
    self.name = 'Untitled'
    self.children = []
    self.position = float3(0.0, 0.0, 0.0)
    self.rotation = float3(0.0, 0.0, 0.0)
    self.scale = float3(1.0, 1.0, 1.0)
    
    matrix = matrix_float4x4.translation_x_y_z_(self.position.x, self.position.y, self.position.z)
    matrix = matrix.rotatedBy_angle_x_y_z_(self.rotation.x, 1.0, 0.0, 0.0)
    matrix = matrix.rotatedBy_angle_x_y_z_(self.rotation.y, 0.0, 1.0, 0.0)
    matrix = matrix.rotatedBy_angle_x_y_z_(self.rotation.z, 0.0, 0.0, 1.0)
    matrix = matrix.scaledBy_x_y_z_(self.scale.x, self.scale.y, self.scale.z)
    self.modelMatrix = matrix

  def add_childNode_(self, childNode):
    self.children.append(childNode)

  def render_commandEncoder_parentModelViewMatrix_(self, commandEncoder, parentModelViewMatrix):
    modelViewMatrix = matrix_multiply(parentModelViewMatrix, self.modelMatrix)
    print(modelViewMatrix)
    
    for child in self.children:
      super().render_commandEncoder_parentModelViewMatrix_(commandEncoder, parentModelViewMatrix)
      child.render_commandEncoder_parentModelViewMatrix_(commandEncoder, parentModelViewMatrix)
      
    self.doRender_commandEncoder_modelViewMatrix_(commandEncoder, self.modelMatrix)
    
    #if self.doRender_commandEncoder_modelViewMatrix_:
      #self.doRender_commandEncoder_modelViewMatrix_(commandEncoder, self.modelMatrix)
