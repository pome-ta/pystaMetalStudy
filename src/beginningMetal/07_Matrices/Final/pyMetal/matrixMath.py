from math import pi, sin, cos, tan
import ctypes



class f4(ctypes.Structure):
  _fields_ = [
    ('ffff', ctypes.c_float * 4),
  ]


class floatX_Y_Z_W(ctypes.Structure):
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
  _fields_ = [('xyzw', floatX_Y_Z_W), ('ffff', f4)]

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

  def __init__(self, c0, c1, c2, c3):
    self.c0 = c0
    self.c1 = c1
    self.c2 = c2
    self.c3 = c3


if __name__ == '__main__':
  f0 = float4(0.0, 0.1, 0.2, 0.3)
  f1 = float4(1.0, 1.1, 1.2, 1.3)
  f2 = float4(2.0, 2.1, 2.2, 2.3)
  f3 = float4(3.0, 3.1, 3.2, 3.3)
  mm = matrix_float4x4(f0, f1, f2, f3)
  #mm.c1 = (1.0, 1.0,1.0,1.0)
  print(mm.m[0])



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
