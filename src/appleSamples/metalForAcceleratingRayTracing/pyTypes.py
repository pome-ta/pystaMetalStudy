import ctypes

from simd.vector3 import Vector3
'''
FACE_MASK_NONE = 0
FACE_MASK_NEGATIVE_X = (1 << 0)
FACE_MASK_POSITIVE_X = (1 << 1)
FACE_MASK_NEGATIVE_Y = (1 << 2)
FACE_MASK_POSITIVE_Y = (1 << 3)
FACE_MASK_NEGATIVE_Z = (1 << 4)
FACE_MASK_POSITIVE_Z = (1 << 5)
FACE_MASK_ALL = ((1 << 6) - 1)
'''


class Camera(ctypes.Structure):
  _fields_ = [
    ('position', Vector3),
    ('right', Vector3),
    ('up', Vector3),
    ('forward', Vector3)
  ]


class AreaLight(ctypes.Structure):
  _fields_ = [
    ('position', Vector3),
    ('forward', Vector3),
    ('right', Vector3),
    ('up', Vector3),
    ('color', Vector3)
  ]


class Uniforms(ctypes.Structure):
  _fields_ = [
    # xxx: `unsigned int`: `ctypes.c_uint16` ?
    ('width', ctypes.c_uint16),
    ('height', ctypes.c_uint16),
    ('frameIndex', ctypes.c_uint16),
    ('camera', Camera),
    ('light', AreaLight)
  ]


if __name__ == '__main__':
  # sizeof: 116
  print(ctypes.sizeof(Uniforms))

