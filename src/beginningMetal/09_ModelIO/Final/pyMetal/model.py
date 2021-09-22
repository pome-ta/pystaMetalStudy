from pathlib import Path
import ctypes

from objc_util import c, ObjCClass, ObjCInstance, nsurl

from .mNode import Node
from .renderable import Renderable
from .texturable import Texturable
from .pyTypes import ModelConstants, Vertex, Position, Color, Texture
from .utils import err_ptr


root_path = Path(__file__).parent / '../' / Path('./Models')

Float = (ctypes.c_float)


class Model(Node, Renderable, Texturable):
  def __init__(self, device=None, modelName=None):
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
    
    self.texture = None
    Texturable.__init__(self)
    imageName = modelName + '.png'
    texture = self.setTexture_device_imageName_(device, imageName)
    self.texture = texture
    self.fragmentFunctionName = "textured_fragment"
    self.rps = self.buildPipelineState(device)
    
  def loadModel_device_modelName_(self, device, modelName):
    assetURL = root_path / modelName / (modelName + '.obj')
    MTKModelIOVertexDescriptorFromMetal = c.MTKModelIOVertexDescriptorFromMetal
    MTKModelIOVertexDescriptorFromMetal.argtypes = [ctypes.c_void_p]
    MTKModelIOVertexDescriptorFromMetal.restype = ctypes.c_void_p

    descriptor = ObjCInstance(MTKModelIOVertexDescriptorFromMetal(self.vertexDescriptor))
    
    attributePosition = descriptor.attributes().objectAtIndex_(0)
    attributePosition.name = 'MDLVertexAttributePosition'
    
    attributeColor = descriptor.attributes().objectAtIndex_(1)
    attributeColor.name = 'MDLVertexAttributeColor'
    
    attributeTexture = descriptor.attributes().objectAtIndex_(2)
    attributeTexture.name = 'MDLVertexAttributeTextureCoordinate'
    
    attributeNormal = descriptor.attributes().objectAtIndex_(3)
    attributeNormal.name = 'MDLVertexAttributeNormal'
    
    
    MTKMeshBufferAllocator = ObjCClass('MTKMeshBufferAllocator').new()
    bufferAllocator = MTKMeshBufferAllocator.initWithDevice_(device)
    MDLAsset = ObjCClass('MDLAsset').new()

    asset = MDLAsset.initWithURL_vertexDescriptor_bufferAllocator_(nsurl(str(assetURL)), descriptor, bufferAllocator)
    self.meshes = ObjCClass('MTKMesh').newMeshesFromAsset_device_sourceMeshes_error_(asset, device, err_ptr, err_ptr)

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

  def doRender_commandEncoder_modelViewMatrix_(self, commandEncoder, modelViewMatrix):
    # todo: 親の`Renderable` が`pass` だけどとりあえず呼んでる
    super().doRender_commandEncoder_modelViewMatrix_(
      commandEncoder, modelViewMatrix)
      
    self.modelConstants.modelViewMatrix = modelViewMatrix
    
    commandEncoder.setVertexBytes_length_atIndex_(
      ctypes.byref(self.modelConstants), ctypes.sizeof(self.modelConstants), 1)

    if self.texture:
      commandEncoder.setFragmentTexture_atIndex_(
        self.texture, 0)
    commandEncoder.setRenderPipelineState_(self.rps)
    
    
    



