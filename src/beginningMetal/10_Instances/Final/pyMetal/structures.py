import ctypes

Position = (ctypes.c_float * 3)
Color = (ctypes.c_float * 4)
Texture = (ctypes.c_float * 2)


class float3(ctypes.Structure):
  _fields_ = [
    ('x', ctypes.c_float),
    ('y', ctypes.c_float),
    ('z',ctypes.c_float)
  ]

  def __str__(self):
    fstr = f'''float3:
      [x:{self.x: .4f}
       y:{self.y: .4f}
       z:{self.z: .4f}]
    '''
    return fstr


class f4(ctypes.Structure):
  _fields_ = [
    ('ffff', ctypes.c_float * 4),
  ]


class float_xyzw(ctypes.Structure):
  _fields_ = [
    ('x', ctypes.c_float),
    ('y', ctypes.c_float),
    ('z', ctypes.c_float),
    ('w', ctypes.c_float),
  ]


class float4(ctypes.Union):
  _anonymous_ = [
    ('xyzw'),
    ('ffff'),
  ]
  _fields_ = [('xyzw', float_xyzw), ('ffff', f4)]

  def __init__(self, x, y, z, w):
    self.x = x
    self.y = y
    self.z = z
    self.w = w


class columns(ctypes.Structure):
  _fields_ = [
    ('c0', float4),
    ('c1', float4),
    ('c2', float4),
    ('c3', float4),
  ]


class float16(ctypes.Structure):
  _fields_ = [
    ('m', (ctypes.c_float * 16)),
  ]


# https://github.com/Cethric/OpenGLES-Pythonista/blob/master/GLKit/glkmath/matrix4.py
class m16(ctypes.Structure):
  _fields_ = [
    ('m00', ctypes.c_float), ('m01', ctypes.c_float), ('m02', ctypes.c_float), ('m03', ctypes.c_float),
    
    ('m10', ctypes.c_float), ('m11', ctypes.c_float), ('m12', ctypes.c_float), ('m13', ctypes.c_float),
    
    ('m20', ctypes.c_float), ('m21', ctypes.c_float), ('m22', ctypes.c_float), ('m23', ctypes.c_float),
    
    ('m30', ctypes.c_float), ('m31', ctypes.c_float), ('m32', ctypes.c_float), ('m33', ctypes.c_float),
  ]


