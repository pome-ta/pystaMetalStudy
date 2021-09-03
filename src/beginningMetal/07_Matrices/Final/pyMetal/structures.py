import ctypes

Position = (ctypes.c_float * 3)
Color = (ctypes.c_float * 4)
Texture = (ctypes.c_float * 2)


class Vertex(ctypes.Structure):
  _fields_ = [('position', Position), ('color', Color), ('texture', Texture)]


class Vertices(ctypes.Structure):
  _fields_ = [('vertex', Vertex * 4)]


class Constants(ctypes.Structure):
  _fields_ = [('animateBy', ctypes.c_float)]

