import ctypes

from .mNode import Node
from .model import Model
from .renderable import Renderable
from .pyTypes import ModelConstants
from .utils import err_ptr


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
    if i in range(instances):
      node = Node()
      node.name = f'Instance {i}'
      self.nodes.append(node)
      self.instanceConstants.append(ModelConstants())

  def makeBuffer(self, device):
    self.instanceBuffer = device.newBufferWithLength_options_(
      ctypes.sizeof(self.modelConstants), 0)
    # xxx: どちらか
    #self.instanceBuffer = device.newBufferWithLength_options_(self.modelConstants.__len__()*ctypes.sizeof(self.modelConstants), 0)
    self.instanceBuffer.label = 'Instance Buffer'
    
  def doRender_commandEncoder_modelViewMatrix_(self, commandEncoder, modelViewMatrix):
    # todo: 親の`Renderable` が`pass` だけどとりあえず呼んでる
    super().doRender_commandEncoder_modelViewMatrix_(commandEncoder, modelViewMatrix)
    
    if len(self.nodes) <= 0:
      return
    instanceBuffer = self.instanceBuffer
    

