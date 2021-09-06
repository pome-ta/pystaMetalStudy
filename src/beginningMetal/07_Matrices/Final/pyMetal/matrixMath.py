from math import pi, sin, cos, tan
import ctypes

class float3(ctypes.Structure):
  _fields_ = [
    ('x', ctypes.c_float),
    ('y', ctypes.c_float),
    ('z', ctypes.c_float),
  ]

class matrix_float3x3(ctypes.Structure):
  _fields_ = [
    ('column0', float3),
    ('column1', float3),
    ('column2', float3),
  ]


class float4(ctypes.Structure):
  _fields_ = [
    ('x', ctypes.c_float),
    ('y', ctypes.c_float),
    ('z', ctypes.c_float),
    ('w', ctypes.c_float),
  ]

class matrix_float4x4(ctypes.Structure):
  _fields_ = [
    ('column0', float4),
    ('column1', float4),
    ('column2', float4),
    ('column3', float4),
  ]


'''
00, 01, 02, 03
10, 11, 12, 13
20, 21, 22, 23
30, 31, 32, 33
'''
'''
 0,  1,  2,  3
 4,  5,  6,  7
 8,  9, 10, 11
12, 13, 14, 15
'''


def matrix_multiply(matrixLeft, matrixRight):
  m = matrix_float4x4()
  print(dir(m))
  print(dir(matrixLeft.column3.w))
  print(matrixLeft.column3[0])
  m.column0[0] = matrixLeft.column0[0] * matrixRight.column0[0]\
               + matrixLeft.column1[0] * matrixRight.column0[1]\
               + matrixLeft.column2[0] * matrixRight.column0[2]\
               + matrixLeft.column3[0] * matrixRight.column0[3]
  
  m.column1[0] = matrixLeft.column0[0] * matrixRight.column1[0]\
               + matrixLeft.column1[0] * matrixRight.column1[1]\
               + matrixLeft.column2[0] * matrixRight.column1[2]\
               + matrixLeft.column3.x * matrixRight.column1.z

'''
def GLKMatrix4Multiply(matrixLeft, matrixRight):
  m = GLKMatrix4()
  
  # ---
  m.m[0] = matrixLeft.m[0] * matrixRight.m[0]
         + matrixLeft.m[4] * matrixRight.m[1]
         + matrixLeft.m[8] * matrixRight.m[2]
         + matrixLeft.m[12] * matrixRight.m[3]
  
  m.m[4] = matrixLeft.m[0] * matrixRight.m[4]
         + matrixLeft.m[4] * matrixRight.m[5]
         + matrixLeft.m[8] * matrixRight.m[6]
         + matrixLeft.m[12] * matrixRight.m[7]
  
  m.m[8] = matrixLeft.m[0] * matrixRight.m[8]
         + matrixLeft.m[4] * matrixRight.m[9]
         + matrixLeft.m[8] * matrixRight.m[10]
         + matrixLeft.m[12] * matrixRight.m[11]
  
  m.m[12] = matrixLeft.m[0] * matrixRight.m[12]
          + matrixLeft.m[4] * matrixRight.m[13]
          + matrixLeft.m[8] * matrixRight.m[14]
          + matrixLeft.m[12] * matrixRight.m[15]

  # ---
  m.m[1] = matrixLeft.m[1] * matrixRight.m[0]
         + matrixLeft.m[5] * matrixRight.m[1]
         + matrixLeft.m[9] * matrixRight.m[2]
         + matrixLeft.m[13] * matrixRight.m[3]
  
  m.m[5] = matrixLeft.m[1] * matrixRight.m[4]
         + matrixLeft.m[5] * matrixRight.m[5] 
         + matrixLeft.m[9] * matrixRight.m[6]
         + matrixLeft.m[13] * matrixRight.m[7]
  
  m.m[9] = matrixLeft.m[1] * matrixRight.m[8]
         + matrixLeft.m[5] * matrixRight.m[9]
         + matrixLeft.m[9] * matrixRight.m[10]
         + matrixLeft.m[13] * matrixRight.m[11]
  
  m.m[13] = matrixLeft.m[1] * matrixRight.m[12]
          + matrixLeft.m[5] * matrixRight.m[13]
          + matrixLeft.m[9] * matrixRight.m[14]
          + matrixLeft.m[13] * matrixRight.m[15]

  # ---
  m.m[2] = matrixLeft.m[2] * matrixRight.m[0]
         + matrixLeft.m[6] * matrixRight.m[1]
         + matrixLeft.m[10] * matrixRight.m[2]
         + matrixLeft.m[14] * matrixRight.m[3]
  
  m.m[6] = matrixLeft.m[2] * matrixRight.m[4]
         + matrixLeft.m[6] * matrixRight.m[5]
         + matrixLeft.m[10] * matrixRight.m[6]
         + matrixLeft.m[14] * matrixRight.m[7]
  
  m.m[10] = matrixLeft.m[2] * matrixRight.m[8]
          + matrixLeft.m[6] * matrixRight.m[9]
          + matrixLeft.m[10] * matrixRight.m[10]
          + matrixLeft.m[14] * matrixRight.m[11]
  
  m.m[14] = matrixLeft.m[2] * matrixRight.m[12]
          + matrixLeft.m[6] * matrixRight.m[13]
          + matrixLeft.m[10] * matrixRight.m[14]
          + matrixLeft.m[14] * matrixRight.m[15]

  # ---
  m.m[3] = matrixLeft.m[3] * matrixRight.m[0]
         + matrixLeft.m[7] * matrixRight.m[1]
         + matrixLeft.m[11] * matrixRight.m[2]
         + matrixLeft.m[15] * matrixRight.m[3]
  
  m.m[7] = matrixLeft.m[3] * matrixRight.m[4]
         + matrixLeft.m[7] * matrixRight.m[5]
         + matrixLeft.m[11] * matrixRight.m[6]
         + matrixLeft.m[15] * matrixRight.m[7]
  
  m.m[11] = matrixLeft.m[3] * matrixRight.m[8]
          + matrixLeft.m[7] * matrixRight.m[9]
          + matrixLeft.m[11] * matrixRight.m[10] 
          + matrixLeft.m[15] * matrixRight.m[11]
  
  m.m[15] = matrixLeft.m[3] * matrixRight.m[12]
          + matrixLeft.m[7] * matrixRight.m[13]
          + matrixLeft.m[11] * matrixRight.m[14]
          + matrixLeft.m[15] * matrixRight.m[15]

  return m


'''



class Matrix_float4x4(matrix_float4x4):
  @classmethod
  def translatedBy_x_y_z_(cls, x, y, z):
    cls.column0 = float4(1.0, 0.0, 0.0, 0.0)
    cls.column1 = float4(0.0, 1.0, 0.0, 0.0)
    cls.column2 = float4(0.0, 0.0, 1.0, 0.0)
    cls.column3 = float4(  x,   y,   z, 0.0)
    return cls()
    
  @classmethod
  def scaledBy_x_y_z_(cls, x, y, z):
    cls.column0 = float4(  x, 0.0, 0.0, 0.0)
    cls.column1 = float4(0.0,   y, 0.0, 0.0)
    cls.column2 = float4(0.0, 0.0,   z, 0.0)
    cls.column3 = float4(0.0, 0.0, 0.0, 0.0)
    return cls()
    
  @classmethod
  def rotatedBy_rotationAngle_x_y_z_(cls, angle, x, y, z):
    c = cos(angle)
    s = sin(angle)
    
    cls.column0 = float4(0.0, 0.0, 0.0, 0.0)
    cls.column0.x = x * x + (1.0 - x * x) * c
    cls.column0.y = x * y * (1.0 - c) - z * s
    cls.column0.z = x * z * (1.0 - c) + y * s
    cls.column0.w = 0
    
    cls.column1 = float4(0.0, 0.0, 0.0, 0.0)
    cls.column1.x = x * y * (1.0 - c) + z * s
    cls.column1.y = y * y + (1.0 - y * y) * c
    cls.column1.z = y * z * (1.0 - c) - x * s
    cls.column1.w = 0.0
    
    cls.column2 = float4(0.0, 0.0, 0.0, 0.0)
    cls.column2.x = x * z * (1.0 - c) - y * s
    cls.column2.y = y * z * (1.0 - c) + x * s
    cls.column2.z = z * z + (1.0 - z * z) * c
    cls.column2.w = 0.0
    
    cls.column3 = float4(0.0, 0.0, 0.0, 1.0)
    return cls()
    
  def projectionFov_aspect_nearZ_farZ_(cls, fov, aspect, nearZ, farZ):
    y = 1.0 / tan(fov * 0.5)
    x = y / aspect
    z = farZ / (nearZ - farZ)
    cls.column0 = float4(  x, 0.0, 0.0, 0.0)
    cls.column1 = float4(0.0,   y, 0.0, 0.0)
    cls.column2 = float4(0.0, 0.0,   z, -1.0)
    cls.column3 = float4(0.0, 0.0, z * nearZ, 0.0)
    
  def upperLeft3x3(self):
    columns0 = float3(self.column0.x, self.column0.y, self.column0.z)
    columns1 = float3(self.column1.x, self.column1.y, self.column1.z)
    columns2 = float3(self.column2.x, self.column2.y, self.column2.z)
    return matrix_float3x3(columns0, columns1, columns2)
    


class ModelConstants(ctypes.Structure):
  _fields_ = [
    ('x', ctypes.c_float * 4),
    ('y', ctypes.c_float * 4),
    ('z', ctypes.c_float * 4),
    ('w', ctypes.c_float * 4),
  ]


class SampleClassMethod:
  def __init__(self):
    self.hoge = '1'
    print('init')

  def fnc(self):
    self.fuga = 2

  @classmethod
  def samle_method(cls):
    return fnc(cls)


if __name__ == '__main__':
  pass
