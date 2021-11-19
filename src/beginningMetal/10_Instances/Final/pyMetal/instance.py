from .mNode import Node
from .model import Model
from .renderable import Renderable
from .pyTypes import ModelConstants


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
    self.instanceBuffer

