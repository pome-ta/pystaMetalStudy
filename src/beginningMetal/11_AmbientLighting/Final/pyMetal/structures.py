import ctypes
from typing import Any



class Float2(ctypes.Structure):
  _fields_ = [
    ('x', ctypes.c_float),
    ('y', ctypes.c_float)
  ]
  
  def __str__(self):
    float2_str = f'''float2:
      [x:{self.x: .4f}
       y:{self.y: .4f}]
    '''
    return float2_str

class Float3(ctypes.Structure):
  _fields_ = [
    ('x', ctypes.c_float),
    ('y', ctypes.c_float),
    ('z', ctypes.c_float)
  ]
  
  def __str__(self):
    float3_str = f'''float3:
      [x:{self.x: .4f}
       y:{self.y: .4f}
       z:{self.z: .4f}]
    '''
    return float3_str


class F4(ctypes.Structure):
  _fields_ = [
    ('ffff', ctypes.c_float * 4),
  ]


class FloatXYZW(ctypes.Structure):
  _fields_ = [
    ('x', ctypes.c_float),
    ('y', ctypes.c_float),
    ('z', ctypes.c_float),
    ('w', ctypes.c_float),
  ]


class Float4(ctypes.Union):
  _anonymous_ = ['xyzw', 'ffff', ]
  _fields_ = [('xyzw', FloatXYZW), ('ffff', F4)]
  
  def __init__(self, x, y, z, w, *args: Any, **kw: Any):
    super().__init__(*args, **kw)
    self.x = x
    self.y = y
    self.z = z
    self.w = w


class Columns(ctypes.Structure):
  _fields_ = [
    ('c0', Float4),
    ('c1', Float4),
    ('c2', Float4),
    ('c3', Float4),
  ]


class Float16(ctypes.Structure):
  _fields_ = [
    ('m', (ctypes.c_float * 16)),
  ]


# https://github.com/Cethric/OpenGLES-Pythonista/blob/master/GLKit/glkmath/matrix4.py
class M16(ctypes.Structure):
  _fields_ = [
    ('m00', ctypes.c_float), ('m01', ctypes.c_float), ('m02', ctypes.c_float), ('m03', ctypes.c_float),
    ('m10', ctypes.c_float), ('m11', ctypes.c_float), ('m12', ctypes.c_float), ('m13', ctypes.c_float),
    ('m20', ctypes.c_float), ('m21', ctypes.c_float), ('m22', ctypes.c_float), ('m23', ctypes.c_float),
    ('m30', ctypes.c_float), ('m31', ctypes.c_float), ('m32', ctypes.c_float), ('m33', ctypes.c_float),
  ]


Position = Float3
Color = Float4
Texture = Float2
