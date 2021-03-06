from math import sin, cos, tan, pi
import ctypes


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
  _fields_ = [
    ('xyzw', float_xyzw),
    ('ffff', f4)
  ]

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
    ('m00', ctypes.c_float),
    ('m01', ctypes.c_float),
    ('m02', ctypes.c_float),
    ('m03', ctypes.c_float),
    ('m10', ctypes.c_float),
    ('m11', ctypes.c_float),
    ('m12', ctypes.c_float),
    ('m13', ctypes.c_float),
    ('m20', ctypes.c_float),
    ('m21', ctypes.c_float),
    ('m22', ctypes.c_float),
    ('m23', ctypes.c_float),
    ('m30', ctypes.c_float),
    ('m31', ctypes.c_float),
    ('m32', ctypes.c_float),
    ('m33', ctypes.c_float),
  ]


class matrix_float4x4(ctypes.Union):
  _anonymous_ = [
    ('columns'),
    ('s1'),
    ('s2'),
  ]
  _fields_ = [
    ('columns', columns),
    ('s1', float16),
    ('s2', m16),
  ]

  def __str__(self):
    valus = [float(x) for x in self.s1.m]
    mstr = f'''matrix_float4x4:
      [{valus[0]:.4f}, {valus[1]:.4f}, {valus[2]:.4f}, {valus[3]:.4f}]
      [{valus[4]:.4f}, {valus[5]:.4f}, {valus[6]:.4f}, {valus[7]:.4f}]
      [{valus[8]:.4f}, {valus[9]:.4f}, {valus[10]:.4f}, {valus[11]:.4f}]
      [{valus[12]:.4f}, {valus[13]:.4f}, {valus[14]:.4f}, {valus[15]:.4f}]'''

    return mstr

  def __init__(self):
    # xxx: `matrix_identity_float4x4` ?
    columns = (
      float4(1.0, 0.0, 0.0, 0.0),
      float4(0.0, 1.0, 0.0, 0.0),
      float4(0.0, 0.0, 1.0, 0.0),
      float4(0.0, 0.0, 0.0, 1.0))
    self.columns = columns

  @staticmethod
  def translation_x_y_z_(x, y, z):
    columns = (
      float4(1.0, 0.0, 0.0, 0.0),
      float4(0.0, 1.0, 0.0, 0.0),
      float4(0.0, 0.0, 1.0, 0.0),
      float4(  x,   y,   z, 1.0))
    matrix = matrix_float4x4()
    matrix.columns = columns
    return matrix

  @staticmethod
  def scale_x_y_z_(x, y, z):
    columns = (
      float4(  x, 0.0, 0.0, 0.0),
      float4(0.0,   y, 0.0, 0.0),
      float4(0.0, 0.0,   z, 0.0),
      float4(0.0, 0.0, 0.0, 1.0))
    matrix = matrix_float4x4()
    matrix.columns = columns
    return matrix

  @staticmethod
  def rotation_angle_x_y_z_(angle, x, y, z):
    c = cos(angle)
    s = sin(angle)

    column0 = float4(0.0, 0.0, 0.0, 0.0)
    column0.x = x * x + (1.0 - x * x) * c
    column0.y = x * y * (1.0 - c) - z * s
    column0.z = x * z * (1.0 - c) + y * s
    column0.w = 0.0

    column1 = float4(0.0, 0.0, 0.0, 0.0)
    column1.x = x * y * (1.0 - c) + z * s
    column1.y = y * y + (1.0 - y * y) * c
    column1.z = y * z * (1.0 - c) - x * s
    column1.w = 0.0

    column2 = float4(0.0, 0.0, 0.0, 0.0)
    column2.x = x * z * (1.0 - c) - y * s
    column2.y = y * z * (1.0 - c) + x * s
    column2.z = z * z + (1.0 - z * z) * c
    column2.w = 0.0

    column3 = float4(0.0, 0.0, 0.0, 1.0)

    matrix = matrix_float4x4()
    columns = (column0, column1, column2, column3)
    matrix.columns = columns
    return matrix

  @staticmethod
  def projection_fov_aspect_nearZ_farZ_(fov, aspect, nearZ, farZ):
    y = 1 / tan(fov * 0.5)
    x = y / aspect
    z = farZ / (nearZ - farZ)

    columns = (
      float4(  x, 0.0, 0.0, 0.0),
      float4(0.0,   y, 0.0, 0.0),
      float4(0.0, 0.0,   z, -1.0),
      float4(0.0, 0.0,   z * nearZ, 0.0))

    matrix = matrix_float4x4()
    matrix.columns = columns
    return matrix


# https://github.com/Cethric/OpenGLES-Pythonista/blob/master/GLKit/glkmath/matrix4.py
def matrix_multiply(matrixLeft, matrixRight):
  matrix = matrix_float4x4()
  matrix.m[
    0] = matrixLeft.m[0] * matrixRight.m[0] + matrixLeft.m[4] * matrixRight.m[1] + matrixLeft.m[8] * matrixRight.m[2] + matrixLeft.m[12] * matrixRight.m[3]
  matrix.m[
    4] = matrixLeft.m[0] * matrixRight.m[4] + matrixLeft.m[4] * matrixRight.m[5] + matrixLeft.m[8] * matrixRight.m[6] + matrixLeft.m[12] * matrixRight.m[7]
  matrix.m[
    8] = matrixLeft.m[0] * matrixRight.m[8] + matrixLeft.m[4] * matrixRight.m[9] + matrixLeft.m[8] * matrixRight.m[10] + matrixLeft.m[12] * matrixRight.m[11]
  matrix.m[
    12] = matrixLeft.m[0] * matrixRight.m[12] + matrixLeft.m[4] * matrixRight.m[13] + matrixLeft.m[8] * matrixRight.m[14] + matrixLeft.m[12] * matrixRight.m[15]

  matrix.m[
    1] = matrixLeft.m[1] * matrixRight.m[0] + matrixLeft.m[5] * matrixRight.m[1] + matrixLeft.m[9] * matrixRight.m[2] + matrixLeft.m[13] * matrixRight.m[3]
  matrix.m[
    5] = matrixLeft.m[1] * matrixRight.m[4] + matrixLeft.m[5] * matrixRight.m[5] + matrixLeft.m[9] * matrixRight.m[6] + matrixLeft.m[13] * matrixRight.m[7]
  matrix.m[
    9] = matrixLeft.m[1] * matrixRight.m[8] + matrixLeft.m[5] * matrixRight.m[9] + matrixLeft.m[9] * matrixRight.m[10] + matrixLeft.m[13] * matrixRight.m[11]
  matrix.m[
    13] = matrixLeft.m[1] * matrixRight.m[12] + matrixLeft.m[5] * matrixRight.m[13] + matrixLeft.m[9] * matrixRight.m[14] + matrixLeft.m[13] * matrixRight.m[15]

  matrix.m[
    2] = matrixLeft.m[2] * matrixRight.m[0] + matrixLeft.m[6] * matrixRight.m[1] + matrixLeft.m[10] * matrixRight.m[2] + matrixLeft.m[14] * matrixRight.m[3]
  matrix.m[
    6] = matrixLeft.m[2] * matrixRight.m[4] + matrixLeft.m[6] * matrixRight.m[5] + matrixLeft.m[10] * matrixRight.m[6] + matrixLeft.m[14] * matrixRight.m[7]
  matrix.m[
    10] = matrixLeft.m[2] * matrixRight.m[8] + matrixLeft.m[6] * matrixRight.m[9] + matrixLeft.m[10] * matrixRight.m[10] + matrixLeft.m[14] * matrixRight.m[11]
  matrix.m[
    14] = matrixLeft.m[2] * matrixRight.m[12] + matrixLeft.m[6] * matrixRight.m[13] + matrixLeft.m[10] * matrixRight.m[14] + matrixLeft.m[14] * matrixRight.m[15]

  matrix.m[
    3] = matrixLeft.m[3] * matrixRight.m[0] + matrixLeft.m[7] * matrixRight.m[1] + matrixLeft.m[11] * matrixRight.m[2] + matrixLeft.m[15] * matrixRight.m[3]
  matrix.m[
    7] = matrixLeft.m[3] * matrixRight.m[4] + matrixLeft.m[7] * matrixRight.m[5] + matrixLeft.m[11] * matrixRight.m[6] + matrixLeft.m[15] * matrixRight.m[7]
  matrix.m[
    11] = matrixLeft.m[3] * matrixRight.m[8] + matrixLeft.m[7] * matrixRight.m[9] + matrixLeft.m[11] * matrixRight.m[10] + matrixLeft.m[15] * matrixRight.m[11]
  matrix.m[
    15] = matrixLeft.m[3] * matrixRight.m[12] + matrixLeft.m[7] * matrixRight.m[13] + matrixLeft.m[11] * matrixRight.m[14] + matrixLeft.m[15] * matrixRight.m[15]

  return matrix


