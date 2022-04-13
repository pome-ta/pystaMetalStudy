import ctypes

from .matrixMath import MatrixFloat4x4 as MatrixIdentityFloat4x4
from .structures import Position, Color, Texture, Float4, Float3, MatrixFloat3x3


class Vertex(ctypes.Structure):
  _fields_ = [('position', Position), ('color', Color), ('texture', Texture)]


# matrix_identity_float4x4 <= 雰囲気
class ModelConstants(ctypes.Structure):
  _pack_ = 16
  _fields_ = [
    ('modelViewMatrix', MatrixIdentityFloat4x4),
    ('materialColor', Float4),
    ('normalMatrix', MatrixFloat3x3),
    ('specularIntensity', ctypes.c_float),
    ('shininess', ctypes.c_float)
  ]


class SceneConstants(ctypes.Structure):
  _fields_ = [
    ('projectionMatrix', MatrixIdentityFloat4x4),
  ]


class Light(ctypes.Structure):
  _fields_ = [
    ('color', Float3),
    ('ambientIntensity', ctypes.c_float),
    ('diffuseIntensity', ctypes.c_float),
    ('direction', Float3)
  ]

