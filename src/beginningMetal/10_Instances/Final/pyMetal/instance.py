import ctypes

from .mNode import Node
from .matrixMath import matrix_multiply
from .model import Model
from .pyTypes import ModelConstants
from .renderable import Renderable

import pdbg


class Instance(Node, Renderable):
  def __init__(self, device=None, modelName=None, instances=None):
    self.model = None
    
    self.nodes = []
    self.instanceConstants = []
    
    self.modelConstants = ModelConstants()
    
    self.instanceBuffer = None
    
    # --- Renderable
    Renderable.__init__(self)
    self.rps = None
    self.vertexFunctionName = 'vertex_instance_shader'
    self.fragmentFunctionName = None
    self.vertexDescriptor = None
    
    self.model = Model(device, modelName)
    self.vertexDescriptor = self.model.vertexDescriptor
    self.fragmentFunctionName = self.model.fragmentFunctionName
    
    Node.__init__(self)
    self.name = modelName
    self.create(instances)
    self.makeBuffer(device)
    self.rps = self.buildPipelineState(device)
  
  def create(self, instances):
    for i in range(instances):
      node = Node()
      node.name = f'Instance {i}'
      self.nodes.append(node)
      self.instanceConstants.append(ModelConstants())
    #print(type(ctypes.byref(self.instanceConstants[0])))
    #print(ctypes.byref(self.instanceConstants[0]))
    #pdbg.state(ctypes.byref(self.instanceConstants[0]))
  
  def makeBuffer(self, device):
    self.instanceBuffer = device.newBufferWithLength_options_(
      len(self.instanceConstants) * ctypes.sizeof(ModelConstants), 0)
    
    self.instanceBuffer.label = 'Instance Buffer'
  
  def doRender_commandEncoder_modelViewMatrix_(self, commandEncoder, modelViewMatrix):
    # todo: 親の`Renderable` が`pass` だけどとりあえず呼んでる
    super().doRender_commandEncoder_modelViewMatrix_(commandEncoder, modelViewMatrix)
    
    if len(self.nodes) <= 0:
      return
    instanceBuffer = self.instanceBuffer
    
    for n, (ic, node) in enumerate(zip(self.instanceConstants, self.nodes)):
      ic.modelViewMatrix = matrix_multiply(modelViewMatrix, node.modelMatrix)
      ic.materialColor = node.materialColor
    
      pointer = instanceBuffer.contents()
      #ctypes.memset(pointer + (ctypes.sizeof(ic) * n), ctypes.byref(ic), ctypes.sizeof(ic))
      ctypes.memset(pointer, ctypes.byref(ic), ctypes.sizeof(ic))
    
    commandEncoder.setFragmentTexture_atIndex_(self.model.texture, 0)
    commandEncoder.setRenderPipelineState_(self.rps)
    commandEncoder.setVertexBuffer_offset_atIndex_(instanceBuffer, 0, 1)
    if len(self.model.meshes) <= 0:
      return
    for mesh in self.model.meshes:
      vertexBuffer = mesh.vertexBuffers().objectAtIndex_(0)
      commandEncoder.setVertexBuffer_offset_atIndex_(vertexBuffer.buffer(), vertexBuffer.offset(), 0)
      for submesh in mesh.submeshes():
        commandEncoder.drawIndexedPrimitives_indexCount_indexType_indexBuffer_indexBufferOffset_instanceCount_(
          submesh.primitiveType(),
          submesh.indexCount(),
          submesh.indexType(),
          submesh.indexBuffer().buffer(),
          submesh.indexBuffer().offset(), len(self.nodes))
