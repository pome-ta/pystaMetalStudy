import ctypes

from .primitive import Primitive
from .pyTypes import Vertex

class Plane(Primitive):
  def buildVertices(self):
    self.vertices = (Vertex * 4)(
      Vertex(position = (-1.0,  1.0,  0.0),
             color    = ( 1.0,  0.0,  0.0,  1.0),
             texture  = ( 0.0,  1.0)),
      Vertex(position = (-1.0, -1.0,  0.0),
             color    = ( 0.0,  1.0,  0.0,  1.0),
             texture  = ( 0.0,  0.0)),
      Vertex(position = ( 1.0, -1.0,  0.0),
             color    = ( 0.0,  0.0,  1.0,  1.0),
             texture  = ( 1.0,  0.0)),
      Vertex(position = ( 1.0,  1.0,  0.0),
             color    = ( 1.0,  0.0,  1.0,  1.0),
             texture  = ( 1.0,  1.0))
    )

    self.indices = (ctypes.c_int16 * 6)(0, 1, 2, 2, 3, 0)
    
