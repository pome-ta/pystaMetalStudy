from simd.vector3 import Vector3, Vector3CrossProduct, Vector3Normalize
from simd.vector4 import Vector4


def getTriangleNormal(v0, v1, v2):
  e1 = Vector3Normalize(v1 - v0)
  e2 = Vector3Normalize(v2 - v0)
  return Vector3CrossProduct(e1, e2)


def createCube(faceMask, color, transform, inwardNormals, triangleMask):
  cubeVertices = [
    Vector3(-0.5, -0.5, -0.5),
    Vector3(0.5, -0.5, -0.5),
    Vector3(-0.5, 0.5, -0.5),
    Vector3(0.5, 0.5, -0.5),
    Vector3(-0.5, -0.5, 0.5),
    Vector3(0.5, -0.5, 0.5),
    Vector3(-0.5, 0.5, 0.5),
    Vector3(0.5, 0.5, 0.5)
  ]

  for i in range(8):
    vertex = cubeVertices[i]
    transformedVertex = Vector4(vertex.x, vertex.y, vertex.z, 1.0)
    print(f'transform: {transform}')
    print(f'transformedVertex: {transformedVertex}')
    transformedVertex = transform * transformedVertex
    print(f'matrixMULvertex: {transformedVertex}')
    xyz = Vector3(
      transformedVertex.x,
      transformedVertex.y,
      transformedVertex.z
    )
    cubeVertices[i] = xyz


if __name__ == '__main__':
  from transforms import matrix4x4_translation, matrix4x4_rotation, matrix4x4_scale

  TRIANGLE_MASK_GEOMETRY = 1
  TRIANGLE_MASK_LIGHT = 2
  RAY_MASK_PRIMARY = 3
  RAY_MASK_SHADOW = 1
  RAY_MASK_SECONDARY = 1

  FACE_MASK_NONE = 0
  FACE_MASK_NEGATIVE_X = (1 << 0)
  FACE_MASK_POSITIVE_X = (1 << 1)
  FACE_MASK_NEGATIVE_Y = (1 << 2)
  FACE_MASK_POSITIVE_Y = (1 << 3)
  FACE_MASK_NEGATIVE_Z = (1 << 4)
  FACE_MASK_POSITIVE_Z = (1 << 5)
  FACE_MASK_ALL = ((1 << 6) - 1)

  transform = matrix4x4_translation(0.0, 1.0, 0.0) * matrix4x4_scale(
    0.5, 1.98, 0.5)

  createCube(FACE_MASK_POSITIVE_Y,
             Vector3(1.0, 1.0, 1.0), transform, True, TRIANGLE_MASK_LIGHT)

