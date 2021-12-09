import math
import ctypes


# from objc_util import parse_struct


class xyzw(ctypes.Structure):
  _fields_ = [
    ('x', ctypes.c_float),
    ('y', ctypes.c_float),
    ('z', ctypes.c_float),
    ('w', ctypes.c_float)
  ]


class rgba(ctypes.Structure):
  _fields_ = [
    ('r', ctypes.c_float),
    ('g', ctypes.c_float),
    ('b', ctypes.c_float),
    ('a', ctypes.c_float)
  ]


class stpq(ctypes.Structure):
  _fields_ = [
    ('s', ctypes.c_float),
    ('t', ctypes.c_float),
    ('p', ctypes.c_float),
    ('q', ctypes.c_float)
  ]


class float4(ctypes.Structure):
  _fields_ = [('v', (ctypes.c_float * 4))]


class Vector4(ctypes.Union):
  _anonymous_ = ['s1', 's2', 's3', 's4', ]
  _fields_ = [
    ('s1', xyzw),
    ('s2', rgba),
    ('s3', stpq),
    ('s4', float4)
  ]

  def __str__(self):
    values = [float(i) for i in self.s4.v]
    vstr = f'''Vector4:
  [{values[0]:.4f}, {values[1]:.4f}, {values[2]:.4f}, {values[3]:.4f}]'''
    return vstr

  def __add__(self, other):
    if isinstance(other, self.__class__):
      return Vector4Add(self, other)
    else:
      raise NotImplementedError()

  def __sub__(self, other):
    if isinstance(other, self.__class__):
      return Vector4Subtract(self, other)
    else:
      raise NotImplementedError()

  def __mul__(self, other):
    if isinstance(other, self.__class__):
      return Vector4Multiply(self, other)
    else:
      raise NotImplementedError()

  def __truediv__(self, other):
    if isinstance(other, self.__class__):
      return Vector4Divide(self, other)
    else:
      raise NotImplementedError()

  def __init__(self, x=0, y=0, z=0, w=0, *args, **kw):
    super().__init__(*args, **kw)
    self.x = x
    self.y = y
    self.z = z
    self.w = w


'''
simd4 = parse_struct('{vec4=ffff}')


def to_simd4(old):
  return ctypes.cast(ctypes.pointer(old), ctypes.POINTER(simd4)).contents


def from_simd4(old):
  return ctypes.cast(ctypes.pointer(old), ctypes.POINTER(Vector4)).contents


def getVector4(func):
  return from_simd4(func(restype=simd4, argtypes=[]))


def setVector4(func, newvalue):
  newvalue = to_simd4(newvalue)
  return func(newvalue, restype=ctypes.c_void_p, argtypes=[simd4])
'''


def Vector4Make(x, y, z, w):
  return Vector4(x=x, y=y, z=z, w=w)


def Vector4MakeWithArray(array):
  return Vector4(v=(ctypes.c_float * 4)(*array))


def Vector4MakeWithVector3(vec3, w):
  return Vector4(x=vec3.x, y=vec3.y, z=vec3.z, w=w)


def Vector4Length(vector):
  v = [float(x) for x in vector.v]
  r = 0
  for x in v:
    r += math.pow(x, 2)
  return math.sqrt(r)


def Vector4Distance(vectorStart, vectorEnd):
  assert isinstance(vectorEnd, Vector4)
  return math.sqrt(
    math.pow(vectorStart.x - vectorEnd.x, 2)
    + math.pow(vectorStart.y - vectorEnd.y, 2)
    + math.pow(vectorStart.z - vectorEnd.z, 2)
    + math.pow(vectorStart.w - vectorEnd.z, 2))


def Vector4Negate(vector):
  v = Vector4()
  v.x = -vector.x
  v.y = -vector.y
  v.z = -vector.z
  v.w = -vector.w
  return v


def Vector4Normalize(vector):
  l = Vector4Length(vector)
  nv = Vector4()
  if l != 0:
    nv.x = vector.x / l
    nv.y = vector.y / l
    nv.z = vector.z / l
    nv.w = vector.w / l
    return nv
  else:
    raise ValueError('Cannot Normalise Vector of length 0')


def Vector4AddScalar(vector, value):
  v = Vector4()
  v.x = vector.x + value
  v.y = vector.y + value
  v.z = vector.z + value
  v.w = vector.w + value
  return v


def Vector4SubtractScalar(vector, value):
  v = Vector4()
  v.x = vector.x - value
  v.y = vector.y - value
  v.z = vector.z - value
  v.w = vector.w - value
  return v


def Vector4MultiplyScalar(vector, value):
  v = Vector4()
  v.x = vector.x * value
  v.y = vector.y * value
  v.z = vector.z * value
  v.w = vector.w * value
  return v


def Vector4DivideScalar(vector, value):
  v = Vector4()
  v.x = vector.x / value
  v.y = vector.y / value
  v.z = vector.z / value
  v.w = vector.w / value
  return v


def Vector4Add(vectorLeft, vectorRight):
  assert isinstance(vectorRight, Vector4)
  v = Vector4()
  v.x = vectorLeft.x + vectorRight.x
  v.y = vectorLeft.y + vectorRight.y
  v.z = vectorLeft.z + vectorRight.z
  v.w = vectorLeft.w + vectorRight.w
  return v


def Vector4Subtract(vectorLeft, vectorRight):
  assert isinstance(vectorRight, Vector4)
  v = Vector4()
  v.x = vectorLeft.x - vectorRight.x
  v.y = vectorLeft.y - vectorRight.y
  v.z = vectorLeft.z - vectorRight.z
  v.w = vectorLeft.w - vectorRight.w
  return v


def Vector4Multiply(vectorLeft, vectorRight):
  assert isinstance(vectorRight, Vector4)
  v = Vector4()
  v.x = vectorLeft.x * vectorRight.x
  v.y = vectorLeft.y * vectorRight.y
  v.z = vectorLeft.z * vectorRight.z
  v.w = vectorLeft.w * vectorRight.w
  return v


def Vector4Divide(vectorLeft, vectorRight):
  assert isinstance(vectorRight, Vector4)
  v = Vector4()
  v.x = vectorLeft.x / vectorRight.x
  v.y = vectorLeft.y / vectorRight.y
  v.z = vectorLeft.z / vectorRight.z
  v.w = vectorLeft.w / vectorRight.w
  return v


def Vector4DotProduct(vectorLeft, vectorRight):
  assert isinstance(vectorRight, Vector4)
  return vectorLeft.x * vectorRight.x + vectorLeft.y * vectorRight.y + vectorLeft.z * vectorRight.z + vectorLeft.w * vectorRight.w


def Vector4CrossProduct(vectorLeft, vectorRight):
  assert isinstance(vectorRight, Vector4)
  v = Vector4()
  v.x = vectorLeft.y * vectorRight.z - vectorLeft.z * vectorRight.y
  v.y = vectorLeft.z * vectorRight.x - vectorLeft.x * vectorRight.z
  v.z = vectorLeft.x * vectorRight.y - vectorLeft.y * vectorRight.x
  v.w = 0
  return v


def Vector4Lerp(vectorStart, vectorEnd, t):
  assert isinstance(vectorEnd, Vector4)
  v = Vector4()
  v.x = vectorStart.x + ((vectorEnd.x - vectorStart.x) * t)
  v.y = vectorStart.y + ((vectorEnd.y - vectorStart.y) * t)
  v.z = vectorStart.z + ((vectorEnd.z - vectorStart.z) * t)
  v.w = vectorStart.w + ((vectorEnd.w - vectorStart.w) * t)


def Vector4Project(vectorToProject, projectionVector):
  assert isinstance(projectionVector, Vector4)
  scale = Vector4DotProduct(projectionVector, vectorToProject)
  scale /= Vector4DotProduct(projectionVector, projectionVector)
  v = Vector4MultiplyScalar(projectionVector, scale)
  return v


def Vector4Maximum(vectorLeft, vectorRight):
  assert isinstance(vectorRight, Vector4)
  v = Vector4()
  v.x = max(vectorLeft.x, vectorRight.x)
  v.y = max(vectorLeft.y, vectorRight.y)
  v.z = max(vectorLeft.z, vectorRight.z)
  v.w = max(vectorLeft.w, vectorRight.w)
  return v


def Vector4Minimum(vectorLeft, vectorRight):
  assert isinstance(vectorRight, Vector4)
  v = Vector4()
  v.x = min(vectorLeft.x, vectorRight.x)
  v.y = min(vectorLeft.y, vectorRight.y)
  v.z = min(vectorLeft.z, vectorRight.z)
  v.w = min(vectorLeft.w, vectorRight.w)
  return v


def Vector4EqualToScalar(vector, value):
  x = vector.x == value
  y = vector.y == value
  z = vector.z == value
  w = vector.w == value
  return x and y and z and w


def Vector4AllEqualToVector4(vectorLeft, vectorRight):
  assert isinstance(vectorRight, Vector4)
  x = vectorLeft.x == vectorRight.x
  y = vectorLeft.y == vectorRight.y
  z = vectorLeft.z == vectorRight.z
  w = vectorLeft.w == vectorRight.w
  return x and y and z and w


def Vector4AllGreaterThanOrEqualToScalar(vector, value):
  x = vector.x >= value
  y = vector.y >= value
  z = vector.z >= value
  w = vector.w >= value
  return x and y and z and w


def Vector4AllGreaterThanOrEqualToVector4(vectorLeft, vectorRight):
  assert isinstance(vectorRight, Vector4)
  x = vectorLeft.x >= vectorRight.x
  y = vectorLeft.y >= vectorRight.y
  z = vectorLeft.z >= vectorRight.z
  w = vectorLeft.w >= vectorRight.w
  return x and y and z and w


def Vector4AllGreaterThanScalar(vector, value):
  x = vector.x > value
  y = vector.y > value
  z = vector.z > value
  w = vector.w > value
  return x and y and z and w


def Vector4AllGreaterThanVector4(vectorLeft, vectorRight):
  assert isinstance(vectorRight, Vector4)
  x = vectorLeft.x > vectorRight.x
  y = vectorLeft.y > vectorRight.y
  z = vectorLeft.z > vectorRight.z
  w = vectorLeft.w > vectorRight.w
  return x and y and z and w


# __all__ = [
#   'Vector4', 'getVector4', 'setVector4', 'Vector4Make', 'Vector4MakeWithArray',
#   'Vector4MakeWithVector3', 'Vector4Length', 'Vector4Distance',
#   'Vector4Negate', 'Vector4Normalize', 'Vector4AddScalar',
#   'Vector4SubtractScalar', 'Vector4MultiplyScalar', 'Vector4DivideScalar',
#   'Vector4Add', 'Vector4Subtract', 'Vector4Multiply', 'Vector4Divide',
#   'Vector4DotProduct', 'Vector4CrossProduct', 'Vector4Lerp', 'Vector4Project',
#   'Vector4Maximum', 'Vector4Minimum', 'Vector4EqualToScalar',
#   'Vector4AllEqualToVector4', 'Vector4AllGreaterThanOrEqualToScalar',
#   'Vector4AllGreaterThanOrEqualToVector4', 'Vector4AllGreaterThanScalar',
#   'Vector4AllGreaterThanVector4'
# ]

__all__ = [
  'Vector4', 'Vector4Make', 'Vector4MakeWithArray',
  'Vector4MakeWithVector3', 'Vector4Length', 'Vector4Distance',
  'Vector4Negate', 'Vector4Normalize', 'Vector4AddScalar',
  'Vector4SubtractScalar', 'Vector4MultiplyScalar', 'Vector4DivideScalar',
  'Vector4Add', 'Vector4Subtract', 'Vector4Multiply', 'Vector4Divide',
  'Vector4DotProduct', 'Vector4CrossProduct', 'Vector4Lerp', 'Vector4Project',
  'Vector4Maximum', 'Vector4Minimum', 'Vector4EqualToScalar',
  'Vector4AllEqualToVector4', 'Vector4AllGreaterThanOrEqualToScalar',
  'Vector4AllGreaterThanOrEqualToVector4', 'Vector4AllGreaterThanScalar',
  'Vector4AllGreaterThanVector4'
]

if __name__ == '__main__':
  v = Vector4Make(1, 1, 1, 1)
  print(v)
  print(Vector4AddScalar(v, 10))
  print(Vector4Length(Vector4Normalize(Vector4AddScalar(v, 10))))
  print(Vector4Minimum(v, Vector4MultiplyScalar(v, 35)))
  print(Vector4Normalize(Vector4AddScalar(v, 10)))
  print(Vector4AllGreaterThanScalar(v, 1.1))
