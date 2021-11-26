import ctypes

from .matrixMath import MatrixFloat4x4 as MatrixIdentityFloat4x4
from .structures import Position, Color, Texture, Float4, Float3


class Vertex(ctypes.Structure):
  _fields_ = [('position', Position), ('color', Color), ('texture', Texture)]


# matrix_identity_float4x4 <= 雰囲気
class ModelConstants(ctypes.Structure):
  _fields_ = [
    ('modelViewMatrix', MatrixIdentityFloat4x4),
    ('materialColor', Float4)
  ]


class SceneConstants(ctypes.Structure):
  _fields_ = [
    ('projectionMatrix', MatrixIdentityFloat4x4),
  ]


class Light(ctypes.Structure):
  _fields_ = [
    ('color', Float3),
    ('ambientIntensity', (ctypes.c_float))
  ]
  
'''
print('Vertex' ,ctypes.sizeof(Vertex))
print('ModelConstants' ,ctypes.sizeof(ModelConstants))
print('SceneConstants' ,ctypes.sizeof(ModelConstants))
print('Light' ,ctypes.sizeof(Light))
print('ctypes.c_float', ctypes.sizeof(ctypes.c_float))
print('Float3', ctypes.sizeof(Float3))
'''
