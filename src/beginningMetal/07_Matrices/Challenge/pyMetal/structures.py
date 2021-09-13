import ctypes

from .matrixMath import matrix_float4x4 as matrix_identity_float4x4


class float3(ctypes.Structure):
  _fields_ = [
    ('x', ctypes.c_float),
    ('y', ctypes.c_float),
    ('z', ctypes.c_float)
  ]
  
  def __str__(self):
    fstr = f'''float3:
      [x:{self.x: .4f}
       y:{self.y: .4f}
       z:{self.z: .4f}]
    '''
    return fstr


Position = (ctypes.c_float * 3)
Color = (ctypes.c_float * 4)
Texture = (ctypes.c_float * 2)


class Vertex(ctypes.Structure):
  _fields_ = [('position', Position), ('color', Color), ('texture', Texture)]


class Vertices(ctypes.Structure):
  _fields_ = [('vertex', Vertex * 4)]


class Constants(ctypes.Structure):
  _fields_ = [('animateBy', ctypes.c_float)]

# matrix_identity_float4x4 <= 雰囲気
class ModelConstants(ctypes.Structure):
  _fields_ = [('modelViewMatrix', matrix_identity_float4x4),]



