import ctypes

from objc_util import ObjCClass

from .mNode import Node
from .renderable import Renderable
from .pyTypes import ModelConstants, Vertex, Position, Color, Texture

Float = (ctypes.c_float)

class Model(Node, Renderable):
  def __init__(self, device, modelName):
    self.meshes = []
    
    # --- Renderable
    Renderable.__init__(self)
    self.rps = None
    self.fragmentFunctionName = 'fragment_shader'
    self.vertexFunctionName = 'vertex_shader'
    self.modelConstants = ModelConstants()
    self.vertexDescriptor = self.__set_vertexDescriptor()
    
    Node.__init__(self)
    self.name = modelName
    self.loadModel_device_modelName_(device, modelName)
    
  def loadModel_device_modelName_(self, device, modelName):
    

  def __set_vertexDescriptor(self):
    vertexDescriptor = ObjCClass('MTLVertexDescriptor').new()
    vertexDescriptor.attributes().objectAtIndexedSubscript_(
      0).format = 30  # .float3
    vertexDescriptor.attributes().objectAtIndexedSubscript_(
      0).offset = 0
    vertexDescriptor.attributes().objectAtIndexedSubscript_(
      0).bufferIndex = 0

    vertexDescriptor.attributes().objectAtIndexedSubscript_(
      1).format = 31  # .float4
    vertexDescriptor.attributes().objectAtIndexedSubscript_(
      1).offset = ctypes.sizeof(Float) * 3
    vertexDescriptor.attributes().objectAtIndexedSubscript_(
      1).bufferIndex = 0

    vertexDescriptor.attributes().objectAtIndexedSubscript_(
      2).format = 29  # .float2
    vertexDescriptor.attributes().objectAtIndexedSubscript_(
      2).offset = ctypes.sizeof(Float) * 7
    vertexDescriptor.attributes().objectAtIndexedSubscript_(
      2).bufferIndex = 0

    vertexDescriptor.attributes().objectAtIndexedSubscript_(
      3).format = 30  # .float3
    vertexDescriptor.attributes().objectAtIndexedSubscript_(
      3).offset = ctypes.sizeof(Float) * 9
    vertexDescriptor.attributes().objectAtIndexedSubscript_(
      3).bufferIndex = 0

    vertexDescriptor.layouts().objectAtIndexedSubscript(
      0).stride = ctypes.sizeof(Float) * 12
    return vertexDescriptor

