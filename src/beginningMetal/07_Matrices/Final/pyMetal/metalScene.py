from .metalNode import Node


class Scene(Node):
  def __init__(self, device, size):
    super().__init__()
    self.device = device
    self.size = size

