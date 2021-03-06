from math import sin
import ctypes

from objc_util import ObjCClass

from .metalNode import Node
from .renderable import Renderable
from .texturable import Texturable
from .structures import *

class Plane(Node, Renderable, Texturable):
  def __init__(self, device, imageName=None, maskImageName=None):
    Node.__init__(self)
    
    self.vertices = Vertices((
      Vertex(
        position=(-1.0,  1.0, 0.0),
        color=(1.0, 0.0, 0.0, 1.0),
        texture=(0.0, 1.0)),
      Vertex(
        position=(-1.0, -1.0, 0.0),
        color=(0.0, 1.0, 0.0, 1.0),
        texture=(0.0, 0.0)),
      Vertex(
        position=( 1.0, -1.0, 0.0),
        color=(0.0, 0.0, 1.0, 1.0),
        texture=(1.0, 0.0)),
      Vertex(
        position=( 1.0,  1.0, 0.0),
        color=(1.0, 0.0, 1.0, 1.0),
        texture=(1.0, 1.0))
    ))
    
    self.indices = (ctypes.c_int16 * 6)(0, 1, 2, 2, 3, 0)
    self.time = 0.0
    self.constants = Constants()

    Renderable.__init__(self)
    self.fragmentFunctionName = 'fragment_shader'
    self.vertexFunctionName = 'vertex_shader'
    self.buildBuffers(device)
    self.vertexDescriptor = self.set_vertexDescriptor()
    self.rps = self.buildPipelineState(device)

    self.texture = None
    self.maskTexture = None
    Texturable.__init__(self)
    # todo: ちょっと気持ち悪いけど、sample に近づける
    if imageName:
      self.init_device_imageName_(device, imageName)

    if maskImageName:
      self.init_device_imageName_maskImageName_(device, imageName, maskImageName)

  def init_device_imageName_(self, device, imageName):
    self.texture = self.setTexture_device_imageName_(device, imageName)
    self.fragmentFunctionName = 'textured_fragment'
    self.buildBuffers(device)
    self.rps = self.buildPipelineState(device)

  def init_device_imageName_maskImageName_(self, device, imageName, maskImageName):
    self.texture = self.setTexture_device_imageName_(device, imageName)
    self.fragmentFunctionName = 'textured_fragment'

    self.maskTexture = self.setTexture_device_imageName_(device, maskImageName)
    self.fragmentFunctionName = 'textured_mask_fragment'
    self.buildBuffers(device)
    self.rps = self.buildPipelineState(device)

  def set_vertexDescriptor(self):
    vertexDescriptor = ObjCClass('MTLVertexDescriptor').new()
    vertexDescriptor.attributes().objectAtIndexedSubscript_(0).format = 30
    vertexDescriptor.attributes().objectAtIndexedSubscript_(0).offset = 0
    vertexDescriptor.attributes().objectAtIndexedSubscript_(0).bufferIndex = 0

    vertexDescriptor.attributes().objectAtIndexedSubscript_(1).format = 31
    vertexDescriptor.attributes().objectAtIndexedSubscript_(
      1).offset = ctypes.sizeof(Position)

    vertexDescriptor.attributes().objectAtIndexedSubscript_(1).bufferIndex = 0

    vertexDescriptor.attributes().objectAtIndexedSubscript_(
      2).format = 29  # .float2
    vertexDescriptor.attributes().objectAtIndexedSubscript_(
      2).offset = ctypes.sizeof(Position) + ctypes.sizeof(Color)
    vertexDescriptor.attributes().objectAtIndexedSubscript_(2).bufferIndex = 0

    vertexDescriptor.layouts().objectAtIndexedSubscript(
      0).stride = ctypes.sizeof(Vertex)
    return vertexDescriptor

  def buildBuffers(self, device):
    self.vertexBuffer = device.newBufferWithBytes_length_options_(
      ctypes.byref(self.vertices), ctypes.sizeof(self.vertices), 0)

    self.indexBuffer = device.newBufferWithBytes_length_options_(
      self.indices, self.indices.__len__() * ctypes.sizeof(self.indices), 0)

  def render_commandEncoder_deltaTime_(self, commandEncoder, deltaTime):
    super().render_commandEncoder_deltaTime_(commandEncoder, deltaTime)
    self.time += deltaTime
    animateBy = abs(sin(self.time) / 2 + 0.5)
    self.constants.animateBy = animateBy

    commandEncoder.setRenderPipelineState_(self.rps)
    commandEncoder.setVertexBuffer_offset_atIndex_(self.vertexBuffer, 0, 0)
    commandEncoder.setVertexBytes_length_atIndex_(
      ctypes.byref(self.constants), ctypes.sizeof(self.constants), 1)

    commandEncoder.setFragmentTexture_atIndex_(self.texture, 0)
    commandEncoder.setFragmentTexture_atIndex_(self.maskTexture, 1)
    commandEncoder.drawIndexedPrimitives_indexCount_indexType_indexBuffer_indexBufferOffset_(
      3, self.indices.__len__(), 0, self.indexBuffer, 0)  # .triangle

