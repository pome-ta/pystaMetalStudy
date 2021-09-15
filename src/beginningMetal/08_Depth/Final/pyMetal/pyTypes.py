import ctypes

from .structures import Position, Color, Texture
from .matrixMath import matrix_float4x4 as matrix_identity_float4x4


class Vertex(ctypes.Structure):
  _fields_ = [('position', Position), ('color', Color), ('texture', Texture)]


# matrix_identity_float4x4 <= 雰囲気
class ModelConstants(ctypes.Structure):
  _fields_ = [
    ('modelViewMatrix', matrix_identity_float4x4),
  ]

