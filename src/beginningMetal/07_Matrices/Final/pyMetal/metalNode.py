class Node:
  def __init__(self):
    self.name = 'Untitled'
    self.children = []

  def add_childNode_(self, childNode):
    self.children.append(childNode)

  def render_commandEncoder_deltaTime_(self, commandEncoder, deltaTime):
    for child in self.children:
      child.render_commandEncoder_deltaTime_(commandEncoder, deltaTime)


