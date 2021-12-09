import math

from simd.vector3 import Vector3, Vector3Normalize
from simd.matrix4 import Matrix4


def matrix4x4_translation(tx, ty, tz):
  return Matrix4(
    (1.0, 0.0, 0.0, 0.0),
    (0.0, 1.0, 0.0, 0.0),
    (0.0, 0.0, 1.0, 0.0),
    (tx, ty, tz, 1.0)
  )


def matrix4x4_rotation(radians, axis):
  # xxx: Vector3 をどこで検知するか？
  if isinstance(axis, Vector3):
    axis = Vector3Normalize(axis)
  else:
    axis = Vector3Normalize(Vector3(*axis))
  ct = math.cos(radians)
  st = math.sin(radians)
  ci = 1 - ct
  x = axis.x
  y = axis.y
  z = axis.z
  return Matrix4(
    (ct + x * x * ci, y * x * ci + z * st, z * x * ci - y * st, 0.0),
    (x * y * ci - z * st, ct + y * y * ci, z * y * ci + x * st, 0.0),
    (x * z * ci + y * st, y * z * ci - x * st, ct + z * z * ci, 0.0),
    (0.0, 0.0, 0.0, 1.0)
  )


def matrix4x4_scale(sx, sy, sz):
  return Matrix4(
    (sx, 0.0, 0.0, 0.0),
    (0.0, sy, 0.0, 0.0),
    (0.0, 0.0, sz, 0.0),
    (0.0, 0.0, 0.0, 1.0)
  )


if __name__ == '__main__':
  testTransform = matrix4x4_translation(0.3275, 0.3, 0.3725)
  print(f'testTransform: {testTransform}')
  testScale = matrix4x4_scale(0.6, 0.6, 0.6)
  print(f'testScale: {testScale}')
  testRotation = matrix4x4_rotation(-0.3, (0.0, 1.0, 0.0))
  print(f'testRotation: {testRotation}')
  transform01 = matrix4x4_translation(0.3275, 0.3, 0.3725) * matrix4x4_rotation(-0.3, Vector3(0.0, 1.0, 0.0)) * matrix4x4_scale( 0.6, 0.6, 0.6)
  print(f'transform01: {transform01}')
  transform02 = matrix4x4_translation(0.0, 1.0, 0.0) * matrix4x4_scale(0.5, 1.98, 0.5)
  print(f'transform02: {transform02}')
