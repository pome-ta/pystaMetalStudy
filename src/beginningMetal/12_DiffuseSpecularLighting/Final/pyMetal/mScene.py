import ctypes

from .camera import Camera
from .mNode import Node
from .pyTypes import SceneConstants, Light


class Scene(Node):
  def __init__(self, device, size):
    super().__init__()
    self.device = device
    self.size = size
    self.camera = Camera()
    self.sceneConstants = SceneConstants()
    self.light = Light()
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
    
    commandEncoder.setFragmentBytes_length_atIndex_(
      ctypes.byref(self.light),
      ctypes.sizeof(Light), 3)
    
    commandEncoder.setVertexBytes_length_atIndex_(
      ctypes.byref(self.sceneConstants),
      ctypes.sizeof(SceneConstants), 2)
    
    for child in self.children:
      child.render_commandEncoder_parentModelViewMatrix_(
        commandEncoder, self.camera.viewMatrix())
  
  def sceneSizeWillChange_size_(self, size):
    width, height = size
    self.camera.aspect = width / height
    
  def touchesBegan_touches_(self, touches):
    pass
    
  def touchesMoved_touches_(self, touches):
    pass
