from math import sin, radians
import ctypes

from objc_util import ObjCClass

from .metalNode import Node
from .renderable import Renderable
from .texturable import Texturable
from .matrixMath import matrix_float4x4, matrix_multiply
from .pyTypes import ModelConstants, Vertex, Position, Color, Texture


class Primitive(Node, Renderable, Texturable):
  def __init__(self, device, imageName=None, maskImageName=None):
    Node.__init__(self)
    self.buildVertices()
    self.time = 0.0
    self.modelConstants = ModelConstants()

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
      self.init_device_imageName_maskImageName_(
        device, imageName, maskImageName)
    

  def set_vertexDescriptor(self):
    vertexDescriptor = ObjCClass('MTLVertexDescriptor').new()
    vertexDescriptor.attributes(
      ).objectAtIndexedSubscript_(0).format = 30
    vertexDescriptor.attributes(
      ).objectAtIndexedSubscript_(0).offset = 0
    vertexDescriptor.attributes(
      ).objectAtIndexedSubscript_(0).bufferIndex = 0

    vertexDescriptor.attributes(
      ).objectAtIndexedSubscript_(1).format = 31
    vertexDescriptor.attributes(
      ).objectAtIndexedSubscript_(1).offset = ctypes.sizeof(Position)

    vertexDescriptor.attributes(
      ).objectAtIndexedSubscript_(1).bufferIndex = 0

    vertexDescriptor.attributes(
      ).objectAtIndexedSubscript_(2).format = 29  # .float2
    vertexDescriptor.attributes(
      ).objectAtIndexedSubscript_(2).offset = ctypes.sizeof(Position) + ctypes.sizeof(Color)
    vertexDescriptor.attributes(
      ).objectAtIndexedSubscript_(2).bufferIndex = 0

    vertexDescriptor.layouts(
      ).objectAtIndexedSubscript(0).stride = ctypes.sizeof(Vertex)
    return vertexDescriptor

  def init_device_imageName_(self, device, imageName):
    self.texture = self.setTexture_device_imageName_(device, imageName)
    self.fragmentFunctionName = 'textured_fragment'
    self.buildBuffers(device)
    self.rps = self.buildPipelineState(device)

  def init_device_imageName_maskImageName_(self, device, imageName, maskImageName):
    self.texture = self.setTexture_device_imageName_(
      device, imageName)
    self.fragmentFunctionName = 'textured_fragment'

    self.maskTexture = self.setTexture_device_imageName_(
      device, maskImageName)
    self.fragmentFunctionName = 'textured_mask_fragment'
    self.buildBuffers(device)
    self.rps = self.buildPipelineState(device)

  def buildVertices(self):
    pass
  
  def buildBuffers(self, device):
    self.vertexBuffer = device.newBufferWithBytes_length_options_(
      ctypes.byref(self.vertices), ctypes.sizeof(self.vertices), 0)

    self.indexBuffer = device.newBufferWithBytes_length_options_(
      self.indices, self.indices.__len__() * ctypes.sizeof(self.indices), 0)

  def doRender_commandEncoder_modelViewMatrix_(self, commandEncoder, modelViewMatrix):
    # todo: 親の`Renderable` が`pass` だけどとりあえず呼んでる
    super().doRender_commandEncoder_modelViewMatrix_(
      commandEncoder, modelViewMatrix)

    if self.indexBuffer:
      indexBuffer = self.indexBuffer
    else:
      return

    # xxx: view size?
    aspect = 414.0 / 804.0
    #aspect = 750.0/1334.0
    projectionMatrix = matrix_float4x4.projection_fov_aspect_nearZ_farZ_(
      radians(65), aspect, 0.1, 100.0)

    self.modelConstants.modelViewMatrix = matrix_multiply(
      projectionMatrix, modelViewMatrix)

    commandEncoder.setRenderPipelineState_(self.rps)
    commandEncoder.setVertexBuffer_offset_atIndex_(
      self.vertexBuffer, 0, 0)
    commandEncoder.setVertexBytes_length_atIndex_(
      ctypes.byref(self.modelConstants), ctypes.sizeof(self.modelConstants), 1)

    commandEncoder.setFragmentTexture_atIndex_(
      self.texture, 0)
    commandEncoder.setFragmentTexture_atIndex_(
      self.maskTexture, 1)

    commandEncoder.setFrontFacingWinding_(1)  # .counterClockwise
    commandEncoder.setCullMode_(2)  # .back
    
    commandEncoder.drawIndexedPrimitives_indexCount_indexType_indexBuffer_indexBufferOffset_(
      3,  # .triangle
      self.indices.__len__(),
      0,
      indexBuffer,
      0)

