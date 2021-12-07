import ctypes
from math import sin, cos, tan
from typing import Any

from structures import Float4, Columns, Float16, M16


class MatrixFloat4x4(ctypes.Union):
  _anonymous_ = ['columns', 's1', 's2']
  _fields_ = [
    ('columns', Columns),
    ('s1', Float16),
    ('s2', M16),
  ]

  def __str__(self):
    valus = [float(x) for x in self.s1.m]
    mstr = f'''matrix_float4x4:
      [{valus[0]:.4f}, {valus[1]:.4f}, {valus[2]:.4f}, {valus[3]:.4f}]
      [{valus[4]:.4f}, {valus[5]:.4f}, {valus[6]:.4f}, {valus[7]:.4f}]
      [{valus[8]:.4f}, {valus[9]:.4f}, {valus[10]:.4f}, {valus[11]:.4f}]
      [{valus[12]:.4f}, {valus[13]:.4f}, {valus[14]:.4f}, {valus[15]:.4f}]'''

    return mstr

  def __init__(self, *args: Any, **kw: Any):
    # xxx: `matrix_identity_float4x4` ?
    super().__init__(*args, **kw)
    columns = (
      Float4(1.0, 0.0, 0.0, 0.0),
      Float4(0.0, 1.0, 0.0, 0.0),
      Float4(0.0, 0.0, 1.0, 0.0),
      Float4(0.0, 0.0, 0.0, 1.0)
    )
    self.columns = columns


#https://github.com/Cethric/OpenGLES-Pythonista/blob/master/GLKit/glkmath/matrix4.py
def matrix_multiply(m_left, m_right):
  matrix = MatrixFloat4x4()
  matrix.m[0] = (m_left.m[0] * m_right.m[0] + m_left.m[4] * m_right.m[1]
                 + m_left.m[8] * m_right.m[2] + m_left.m[12] * m_right.m[3])
  matrix.m[4] = (m_left.m[0] * m_right.m[4] + m_left.m[4] * m_right.m[5]
                 + m_left.m[8] * m_right.m[6] + m_left.m[12] * m_right.m[7])
  matrix.m[8] = (m_left.m[0] * m_right.m[8] + m_left.m[4] * m_right.m[9]
                 + m_left.m[8] * m_right.m[10] + m_left.m[12] * m_right.m[11])
  matrix.m[12] = (m_left.m[0] * m_right.m[12] + m_left.m[4] * m_right.m[13]
                  + m_left.m[8] * m_right.m[14] + m_left.m[12] * m_right.m[15])
  
  matrix.m[1] = (m_left.m[1] * m_right.m[0] + m_left.m[5] * m_right.m[1]
                 + m_left.m[9] * m_right.m[2] + m_left.m[13] * m_right.m[3])
  matrix.m[5] = (m_left.m[1] * m_right.m[4] + m_left.m[5] * m_right.m[5]
                 + m_left.m[9] * m_right.m[6] + m_left.m[13] * m_right.m[7])
  matrix.m[9] = (m_left.m[1] * m_right.m[8] + m_left.m[5] * m_right.m[9]
                 + m_left.m[9] * m_right.m[10] + m_left.m[13] * m_right.m[11])
  matrix.m[13] = (m_left.m[1] * m_right.m[12] + m_left.m[5] * m_right.m[13]
                  + m_left.m[9] * m_right.m[14] + m_left.m[13] * m_right.m[15])
  
  matrix.m[2] = (m_left.m[2] * m_right.m[0] + m_left.m[6] * m_right.m[1]
                 + m_left.m[10] * m_right.m[2] + m_left.m[14] * m_right.m[3])
  matrix.m[6] = (m_left.m[2] * m_right.m[4] + m_left.m[6] * m_right.m[5]
                 + m_left.m[10] * m_right.m[6] + m_left.m[14] * m_right.m[7])
  matrix.m[10] = (m_left.m[2] * m_right.m[8] + m_left.m[6] * m_right.m[9]
                  + m_left.m[10] * m_right.m[10] + m_left.m[14] * m_right.m[11])
  matrix.m[14] = (m_left.m[2] * m_right.m[12] + m_left.m[6] * m_right.m[13]
                  + m_left.m[10] * m_right.m[14] + m_left.m[14] * m_right.m[15])
  
  matrix.m[3] = (m_left.m[3] * m_right.m[0] + m_left.m[7] * m_right.m[1]
                 + m_left.m[11] * m_right.m[2] + m_left.m[15] * m_right.m[3])
  matrix.m[7] = (m_left.m[3] * m_right.m[4] + m_left.m[7] * m_right.m[5]
                 + m_left.m[11] * m_right.m[6] + m_left.m[15] * m_right.m[7])
  matrix.m[11] = (m_left.m[3] * m_right.m[8] + m_left.m[7] * m_right.m[9]
                  + m_left.m[11] * m_right.m[10] + m_left.m[15] * m_right.m[11])
  matrix.m[15] = (m_left.m[3] * m_right.m[12] + m_left.m[7] * m_right.m[13]
                  + m_left.m[11] * m_right.m[14] + m_left.m[15] * m_right.m[15])
  
  return matrix


def matrix4x4_translation(tx, ty, tz):
  columns = (
    Float4(1.0, 0.0, 0.0, 0.0),
    Float4(0.0, 1.0, 0.0, 0.0),
    Float4(0.0, 0.0, 1.0, 0.0),
    Float4(tx, ty, tz, 1.0)
  )
  matrix = MatrixFloat4x4()
  matrix.columns = columns
  return matrix


def matrix4x4_rotation(angle, axis):
  x, y, z = axis
  ct = cos(angle)
  st = sin(angle)
  ci = 1 - ct

  column0 = Float4(0.0, 0.0, 0.0, 0.0)
  column0.x = ct + x * x * ci
  column0.y = y * x * ci + z * st
  column0.z = z * x * ci - y * st
  column0.w = 0.0

  column1 = Float4(0.0, 0.0, 0.0, 0.0)
  column1.x = x * y * ci - z * st
  column1.y = ct + y * y * ci
  column1.z = z * y * ci + x * st
  column1.w = 0.0

  column2 = Float4(0.0, 0.0, 0.0, 0.0)
  column2.x = x * z * ci + y * st
  column2.y = y * z * ci - x * st
  column2.z = ct + z * z * ci
  column2.w = 0.0

  column3 = Float4(0.0, 0.0, 0.0, 1.0)

  matrix = MatrixFloat4x4()
  columns = (column0, column1, column2, column3)
  matrix.columns = columns
  return matrix


def matrix4x4_scale(sx, sy, sz):
  columns = (
    Float4(sx, 0.0, 0.0, 0.0),
    Float4(0.0, sy, 0.0, 0.0),
    Float4(0.0, 0.0, sz, 0.0),
    Float4(0.0, 0.0, 0.0, 1.0)
  )
  matrix = MatrixFloat4x4()
  matrix.columns = columns
  return matrix


def min_max(l):
  l_min = min(l)
  l_max = max(l)
  return [(i - l_min) / (l_max - l_min) for i in l]



if __name__ == '__main__':
  testTransform = matrix4x4_translation(0.3275, 0.3, 0.3725)
  testScale = matrix4x4_scale(0.6, 0.6, 0.6)
  testRotation = matrix4x4_rotation(-0.3, (0.0, 1.0, 0.0))
  #print(testTransform)
  #print(testScale)
  #print(testRotation)
  
  _transform = matrix_multiply(testTransform, testRotation)
  transform = matrix_multiply(matrix_multiply(testTransform, testRotation), testScale)
  
  
  print(transform)
  

