import math
import ctypes


# from objc_util import parse_struct


class xyz(ctypes.Structure):
  _fields_ = [
    ('x', ctypes.c_float),
    ('y', ctypes.c_float),
    ('z', ctypes.c_float)
  ]


class rgb(ctypes.Structure):
  _fields_ = [
    ('r', ctypes.c_float),
    ('g', ctypes.c_float),
    ('b', ctypes.c_float)
  ]


class stp(ctypes.Structure):
  _fields_ = [
    ('s', ctypes.c_float),
    ('t', ctypes.c_float),
    ('p', ctypes.c_float)
  ]


class float3(ctypes.Structure):
  _fields_ = [('v', ctypes.c_float * 3)]


class Vector3(ctypes.Union):
  _anonymous_ = ['s1', 's2', 's3', 's4', ]
  _fields_ = [
    ('s1', xyz),
    ('s2', rgb),
    ('s3', stp),
    ('s4', float3)
  ]

  def __str__(self):
    values = [float(i) for i in self.s4.v]
    vstr = f'''Vector3:
  [{values[0]:.4f}, {values[1]:.4f}, {values[2]:.4f}] '''
    return vstr

  def __add__(self, other):
    if isinstance(other, self.__class__):
      return Vector3Add(self, other)
    else:
      raise NotImplementedError()

  def __sub__(self, other):
    if isinstance(other, self.__class__):
      return Vector3Subtract(self, other)
    else:
      raise NotImplementedError()

  def __mul__(self, other):
    if isinstance(other, self.__class__):
      return Vector3Multiply(self, other)
    else:
      raise NotImplementedError()

  def __truediv__(self, other):
    if isinstance(other, self.__class__):
      return Vector3Divide(self, other)
    else:
      raise NotImplementedError()

  def __init__(self, x=0, y=0, z=0, *args, **kw):
    super().__init__(*args, **kw)
    self.x = x
    self.y = y
    self.z = z


'''
simd3 = parse_struct('{simd3=fff}')


def to_simd3(old):
  return ctypes.cast(ctypes.pointer(old), ctypes.POINTER(simd3)).contents


def from_simd3(old):
  return ctypes.cast(ctypes.pointer(old), ctypes.POINTER(Vector3)).contents


def getVector3(func):
  return from_simd3(func(restype=simd3, argtypes=[]))


def setVector3(func, newvalue):
  newvalue = to_simd3(newvalue)
  return func(newvalue, restype=ctypes.c_void_p, argtypes=[simd3])
'''


def Vector3Make(x, y, z):
  return Vector3(x=x, y=y, z=z)


def Vector3MakeWithArray(values):
  return Vector3(v=(ctypes.c_float * 3)(*values))


def Vector3Length(vector):
  v = [float(x) for x in vector.v]
  r = 0
  for x in v:
    r += math.pow(x, 2)
  return math.sqrt(r)


def Vector3Distance(vectorStart, vectorEnd):
  assert isinstance(vectorEnd, Vector3)
  return math.sqrt(
    math.pow(vectorStart.x - vectorEnd.x, 2)
    + math.pow(vectorStart.y - vectorEnd.y, 2)
    + math.pow(vectorStart.z - vectorEnd.z, 2))


def Vector3Negate(vector):
  v = Vector3()
  v.x = -vector.x
  v.y = -vector.y
  v.z = -vector.z
  return v


def Vector3Normalize(vector):
  l = Vector3Length(vector)
  nv = Vector3()
  if l != 0:
    nv.x = vector.x / l
    nv.y = vector.y / l
    nv.z = vector.z / l
    return nv
  else:
    raise ValueError('Cannot Normalise Vector of length 0')


def Vector3AddScalar(vector, value):
  v = Vector3()
  v.x = vector.x + value
  v.y = vector.y + value
  v.z = vector.z + value
  return v


def Vector3SubtractScalar(vector, value):
  v = Vector3()
  v.x = vector.x - value
  v.y = vector.y - value
  v.z = vector.z - value
  return v


def Vector3MultiplyScalar(vector, value):
  v = Vector3()
  v.x = vector.x * value
  v.y = vector.y * value
  v.z = vector.z * value
  return v


def Vector3DivideScalar(vector, value):
  v = Vector3()
  v.x = vector.x / value
  v.y = vector.y / value
  v.z = vector.z / value
  return v


def Vector3Add(vectorLeft, vectorRight):
  assert isinstance(vectorRight, Vector3)
  v = Vector3()
  v.x = vectorLeft.x + vectorRight.x
  v.y = vectorLeft.y + vectorRight.y
  v.z = vectorLeft.z + vectorRight.z
  return v


def Vector3Subtract(vectorLeft, vectorRight):
  assert isinstance(vectorRight, Vector3)
  v = Vector3()
  v.x = vectorLeft.x - vectorRight.x
  v.y = vectorLeft.y - vectorRight.y
  v.z = vectorLeft.z - vectorRight.z
  return v


def Vector3Multiply(vectorLeft, vectorRight):
  assert isinstance(vectorRight, Vector3)
  v = Vector3()
  v.x = vectorLeft.x * vectorRight.x
  v.y = vectorLeft.y * vectorRight.y
  v.z = vectorLeft.z * vectorRight.z
  return v


def Vector3Divide(vectorLeft, vectorRight):
  assert isinstance(vectorRight, Vector3)
  v = Vector3()
  v.x = vectorLeft.x / vectorRight.x
  v.y = vectorLeft.y / vectorRight.y
  v.z = vectorLeft.z / vectorRight.z
  return v


def Vector3DotProduct(vectorLeft, vectorRight):
  assert isinstance(vectorRight, Vector3)
  return vectorLeft.x * vectorRight.x + vectorLeft.y * vectorRight.y + vectorLeft.z * vectorRight.z


def Vector3CrossProduct(vectorLeft, vectorRight):
  assert isinstance(vectorRight, Vector3)
  v = Vector3()
  v.x = vectorLeft.y * vectorRight.z - vectorLeft.z * vectorRight.y
  v.y = vectorLeft.z * vectorRight.x - vectorLeft.x * vectorRight.z
  v.z = vectorLeft.x * vectorRight.y - vectorLeft.y * vectorRight.x
  return v


def Vector3Lerp(vectorStart, vectorEnd, t):
  assert isinstance(vectorEnd, Vector3)
  v = Vector3()
  v.x = vectorStart.x + ((vectorEnd.x - vectorStart.x) * t)
  v.y = vectorStart.y + ((vectorEnd.y - vectorStart.y) * t)
  v.z = vectorStart.z + ((vectorEnd.z - vectorStart.z) * t)


def Vector3Project(vectorToProject, projectionVector):
  assert isinstance(projectionVector, Vector3)
  scale = Vector3DotProduct(projectionVector, vectorToProject)
  scale /= Vector3DotProduct(projectionVector, projectionVector)
  v = Vector3MultiplyScalar(projectionVector, scale)
  return v


def Vector3Maximum(vectorLeft, vectorRight):
  assert isinstance(vectorRight, Vector3)
  v = Vector3()
  v.x = max(vectorLeft.x, vectorRight.x)
  v.y = max(vectorLeft.y, vectorRight.y)
  v.z = max(vectorLeft.z, vectorRight.z)
  return v


def Vector3Minimum(vectorLeft, vectorRight):
  assert isinstance(vectorRight, Vector3)
  v = Vector3()
  v.x = min(vectorLeft.x, vectorRight.x)
  v.y = min(vectorLeft.y, vectorRight.y)
  v.z = min(vectorLeft.z, vectorRight.z)
  return v


def Vector3EqualToScalar(vector, value):
  x = vector.x == value
  y = vector.y == value
  z = vector.z == value
  return x and y and z


def Vector3AllEqualToVector4(vectorLeft, vectorRight):
  assert isinstance(vectorRight, Vector3)
  x = vectorLeft.x == vectorRight.x
  y = vectorLeft.y == vectorRight.y
  z = vectorLeft.z == vectorRight.z
  return x and y and z


def Vector3AllGreaterThanOrEqualToScalar(vector, value):
  x = vector.x >= value
  y = vector.y >= value
  z = vector.z >= value
  return x and y and z


def Vector3AllGreaterThanOrEqualToVector4(vectorLeft, vectorRight):
  assert isinstance(vectorRight, Vector3)
  x = vectorLeft.x >= vectorRight.x
  y = vectorLeft.y >= vectorRight.y
  z = vectorLeft.z >= vectorRight.z
  return x and y and z


def Vector3AllGreaterThanScalar(vector, value):
  x = vector.x > value
  y = vector.y > value
  z = vector.z > value
  return x and y and z


def Vector3AllGreaterThanVector4(vectorLeft, vectorRight):
  assert isinstance(vectorRight, Vector3)
  x = vectorLeft.x > vectorRight.x
  y = vectorLeft.y > vectorRight.y
  z = vectorLeft.z > vectorRight.z
  return x and y and z


#
# __all__ = [
#   'Vector3', 'setVector3', 'getVector3', 'Vector3Make', 'Vector3MakeWithArray',
#   'Vector3Length', 'Vector3Distance', 'Vector3Negate', 'Vector3Normalize',
#   'Vector3AddScalar', 'Vector3SubtractScalar', 'Vector3MultiplyScalar',
#   'Vector3DivideScalar', 'Vector3Add', 'Vector3Subtract', 'Vector3Multiply',
#   'Vector3Divide', 'Vector3DotProduct', 'Vector3CrossProduct', 'Vector3Lerp',
#   'Vector3Project', 'Vector3Maximum', 'Vector3Minimum', 'Vector3EqualToScalar',
#   'Vector3AllEqualToVector4', 'Vector3AllGreaterThanOrEqualToScalar',
#   'Vector3AllGreaterThanOrEqualToVector4', 'Vector3AllGreaterThanScalar',
#   'Vector3AllGreaterThanVector4'
# ]

__all__ = [
  'Vector3', 'Vector3Make', 'Vector3MakeWithArray',
  'Vector3Length', 'Vector3Distance', 'Vector3Negate', 'Vector3Normalize',
  'Vector3AddScalar', 'Vector3SubtractScalar', 'Vector3MultiplyScalar',
  'Vector3DivideScalar', 'Vector3Add', 'Vector3Subtract', 'Vector3Multiply',
  'Vector3Divide', 'Vector3DotProduct', 'Vector3CrossProduct', 'Vector3Lerp',
  'Vector3Project', 'Vector3Maximum', 'Vector3Minimum', 'Vector3EqualToScalar',
  'Vector3AllEqualToVector4', 'Vector3AllGreaterThanOrEqualToScalar',
  'Vector3AllGreaterThanOrEqualToVector4', 'Vector3AllGreaterThanScalar',
  'Vector3AllGreaterThanVector4'
]

if __name__ == '__main__':
  '''
  v = Vector3Make(1, 1, 1)
  print(v)
  print(Vector3AddScalar(v, 10))
  print(Vector3Length(Vector3Normalize(Vector3AddScalar(v, 10))))
  print(Vector3Minimum(v, Vector3MultiplyScalar(v, 35)))
  print(Vector3Normalize(Vector3AddScalar(v, 10)))
  print(Vector3AllGreaterThanScalar(v, 1.1))
  v1 = Vector3Make(5, 0, 0)
  print(Vector3Length(v1))
  '''
  r_vec3 = Vector3(3.0, 2.0, 1.0)
  l_vec3 = Vector3(2.0, 1.0, 3.0)
  print(r_vec3 - l_vec3)
