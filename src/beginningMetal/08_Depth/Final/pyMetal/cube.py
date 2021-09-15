import ctypes

from .primitive import Primitive
from .structures import *


class Cube(Primitive):
  def buildVertices(self):
    self.vertices = (Vertex * 8)(
      Vertex(
        position=(-1.0,  1.0, 1.0),  # 0 Front
        color=(1.0, 0.0, 0.0, 1.0),
        texture=(0.0, 0.0)),
      Vertex(
        position=(-1.0, -1.0, 1.0),  # 1
        color=(0.0, 1.0, 0.0, 1.0),
        texture=(0.0, 1.0)),
      Vertex(
        position=( 1.0, -1.0, 1.0),  # 2
        color=(0.0, 0.0, 1.0, 1.0),
        texture=(1.0, 0.0)),
      Vertex(
        position=( 1.0,  1.0, 11.0),  # 3
        color=(1.0, 0.0, 1.0, 1.0),
        texture=(1.0, 0.0)),
        
      Vertex(
        position=(-1.0,  1.0, -1.0),  # 4 Back
        color=(0.0, 0.0, 1.0, 1.0),
        texture=(1.0, 1.0)),
      Vertex(
        position=(-1.0, -1.0, -1.0),  # 5
        color=(0.0, 1.0, 0.0, 1.0),
        texture=(0.0, 1.0)),
      Vertex(
        position=( 1.0, -1.0, -1.0),  # 6
        color=(1.0, 0.0, 0.0, 1.0),
        texture=(0.0, 0.0)),
      Vertex(
        position=( 1.0,  1.0, -1.0),  # 7
        color=(1.0, 0.0, 1.0, 1.0),
        texture=(1.0, 0.0))
      )
    self.indices = (ctypes.c_int16 * 36)(
      0, 1, 2,   0, 2, 3,  # Front
      4, 5, 6,   4, 7, 6,  # Back
      
      4, 5, 1,   4, 1, 0,  # Left
      3, 6, 7,   3, 2, 6,  # Right
      
      4, 0, 3,   4, 3, 7,  # Top
      1, 5, 6,   1, 6, 2,  # Bottom
      )
