import ctypes
from .vector4 import Vector4


class float16(ctypes.Structure):
  _fields_ = [
    ('m', ctypes.c_float * 16)
  ]


class m16(ctypes.Structure):
  _fields_ = [
    ('m00', ctypes.c_float), ('m01', ctypes.c_float), ('m02', ctypes.c_float), ('m03', ctypes.c_float),
    ('m10', ctypes.c_float), ('m11', ctypes.c_float), ('m12', ctypes.c_float), ('m13', ctypes.c_float),
    ('m20', ctypes.c_float), ('m21', ctypes.c_float), ('m22', ctypes.c_float), ('m23', ctypes.c_float),
    ('m30', ctypes.c_float), ('m31', ctypes.c_float), ('m32', ctypes.c_float), ('m33', ctypes.c_float)
  ]


class columns(ctypes.Structure):
  _fields_ = [
    ('c0', Vector4),
    ('c1', Vector4),
    ('c2', Vector4),
    ('c3', Vector4)
  ]


class Matrix4(ctypes.Union):
  _anonymous_ = ['columns', 's1', 's2']
  _fields_ = [
    ('columns', columns),
    ('s1', float16),
    ('s2', m16)
  ]

  def __str__(self):
    values = [float(x) for x in self.s1.m]
    mstr = f'''Matrix4:
  [{values[0]:.4f}, {values[1]:.4f}, {values[2]:.4f}, {values[3]:.4f}]
  [{values[4]:.4f}, {values[5]:.4f}, {values[6]:.4f}, {values[7]:.4f}]
  [{values[8]:.4f}, {values[9]:.4f}, {values[10]:.4f}, {values[11]:.4f}]
  [{values[12]:.4f}, {values[13]:.4f}, {values[14]:.4f}, {values[15]:.4f}]'''
    return mstr

  def __mul__(self, other):
    if isinstance(other, self.__class__):
      return Matrix4Multiply(self, other)
    else:
      raise NotImplementedError()

  def __init__(self,
               col_x=(1.0, 0.0, 0.0, 0.0),
               col_y=(0.0, 1.0, 0.0, 0.0),
               col_z=(0.0, 0.0, 1.0, 0.0),
               col_w=(0.0, 0.0, 0.0, 1.0),
               *args, **kw):
    super().__init__(*args, **kw)
    cols = (Vector4(*col_x), Vector4(*col_y), Vector4(*col_z), Vector4(*col_w))
    self.columns = cols


def Matrix4Multiply(matrixLeft, matrixRight):
  m = Matrix4()
  m.m[0] = (matrixLeft.m[0] * matrixRight.m[0] + matrixLeft.m[4] * matrixRight.m[1]
            + matrixLeft.m[8] * matrixRight.m[2] + matrixLeft.m[12] * matrixRight.m[3])
  m.m[4] = (matrixLeft.m[0] * matrixRight.m[4] + matrixLeft.m[4] * matrixRight.m[5]
            + matrixLeft.m[8] * matrixRight.m[6] + matrixLeft.m[12] * matrixRight.m[7])
  m.m[8] = (matrixLeft.m[0] * matrixRight.m[8] + matrixLeft.m[4] * matrixRight.m[9]
            + matrixLeft.m[8] * matrixRight.m[10] + matrixLeft.m[12] * matrixRight.m[11])
  m.m[12] = (matrixLeft.m[0] * matrixRight.m[12] + matrixLeft.m[4] * matrixRight.m[13]
             + matrixLeft.m[8] * matrixRight.m[14] + matrixLeft.m[12] * matrixRight.m[15])

  m.m[1] = (matrixLeft.m[1] * matrixRight.m[0] + matrixLeft.m[5] * matrixRight.m[1]
            + matrixLeft.m[9] * matrixRight.m[2] + matrixLeft.m[13] * matrixRight.m[3])
  m.m[5] = (matrixLeft.m[1] * matrixRight.m[4] + matrixLeft.m[5] * matrixRight.m[5]
            + matrixLeft.m[9] * matrixRight.m[6] + matrixLeft.m[13] * matrixRight.m[7])
  m.m[9] = (matrixLeft.m[1] * matrixRight.m[8] + matrixLeft.m[5] * matrixRight.m[9]
            + matrixLeft.m[9] * matrixRight.m[10] + matrixLeft.m[13] * matrixRight.m[11])
  m.m[13] = (matrixLeft.m[1] * matrixRight.m[12] + matrixLeft.m[5] * matrixRight.m[13]
             + matrixLeft.m[9] * matrixRight.m[14] + matrixLeft.m[13] * matrixRight.m[15])

  m.m[2] = (matrixLeft.m[2] * matrixRight.m[0] + matrixLeft.m[6] * matrixRight.m[1]
            + matrixLeft.m[10] * matrixRight.m[2] + matrixLeft.m[14] * matrixRight.m[3])
  m.m[6] = (matrixLeft.m[2] * matrixRight.m[4] + matrixLeft.m[6] * matrixRight.m[5]
            + matrixLeft.m[10] * matrixRight.m[6] + matrixLeft.m[14] * matrixRight.m[7])
  m.m[10] = (matrixLeft.m[2] * matrixRight.m[8] + matrixLeft.m[6] * matrixRight.m[9]
             + matrixLeft.m[10] * matrixRight.m[10] + matrixLeft.m[14] * matrixRight.m[11])
  m.m[14] = (matrixLeft.m[2] * matrixRight.m[12] + matrixLeft.m[6] * matrixRight.m[13]
             + matrixLeft.m[10] * matrixRight.m[14] + matrixLeft.m[14] * matrixRight.m[15])

  m.m[3] = (matrixLeft.m[3] * matrixRight.m[0] + matrixLeft.m[7] * matrixRight.m[1]
            + matrixLeft.m[11] * matrixRight.m[2] + matrixLeft.m[15] * matrixRight.m[3])
  m.m[7] = (matrixLeft.m[3] * matrixRight.m[4] + matrixLeft.m[7] * matrixRight.m[5]
            + matrixLeft.m[11] * matrixRight.m[6] + matrixLeft.m[15] * matrixRight.m[7])
  m.m[11] = (matrixLeft.m[3] * matrixRight.m[8] + matrixLeft.m[7] * matrixRight.m[9]
             + matrixLeft.m[11] * matrixRight.m[10] + matrixLeft.m[15] * matrixRight.m[11])
  m.m[15] = (matrixLeft.m[3] * matrixRight.m[12] + matrixLeft.m[7] * matrixRight.m[13]
             + matrixLeft.m[11] * matrixRight.m[14] + matrixLeft.m[15] * matrixRight.m[15])

  return m


if __name__ == '__main__':
  m4 = Matrix4()
  print(m4)
