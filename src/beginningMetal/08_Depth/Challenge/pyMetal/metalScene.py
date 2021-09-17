import ctypes

from .metalNode import Node
from .camera import Camera
from .matrixMath import matrix_float4x4
from .pyTypes import SceneConstants


class Scene(Node):
  def __init__(self, device, size):
    super().__init__()
    self.device = device
    self.size = size
    self.camera = Camera()
    self.sceneConstants = SceneConstants()
    self.deltaTime = None
    
    # todo: self.size = bounds(x, y, width, height)
    self.camera.aspect = self.size[2] / self.size[3]
    self.camera.position.z = -6.0
    self.add_childNode_(self.camera)

  def update_deltaTime_(self, deltaTime):
    pass

  def render_commandEncoder_deltaTime_(self, commandEncoder, deltaTime):
    self.update_deltaTime_(deltaTime)
    self.sceneConstants.projectionMatrix = self.camera.projectionMatrix()
    print(self.sceneConstants.projectionMatrix)
    commandEncoder.setVertexBytes_length_atIndex_(
      ctypes.byref(self.sceneConstants),
      ctypes.sizeof(self.sceneConstants), 2)
    
    for child in self.children:
      child.render_commandEncoder_parentModelViewMatrix_(
        commandEncoder, self.camera.viewMatrix())

