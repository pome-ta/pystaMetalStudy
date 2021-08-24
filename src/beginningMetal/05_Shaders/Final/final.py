from pathlib import Path
from math import sin
import ctypes

import numpy as np

from objc_util import c, create_objc_class, ObjCClass, ObjCInstance
import ui


# --- get Shader path
shader_path = Path('./Shader.metal')

wenderlichGreen = (0.0, 0.4, 0.21, 1.0)
err_ptr = ctypes.c_void_p()

Position = (ctypes.c_float * 3)
Color = (ctypes.c_float * 4)


class Vertex(ctypes.Structure):
  _fields_ = [('position', Position), ('color', Color)]


class Vertices(ctypes.Structure):
  _fields_ = [('vertex', Vertex * 4)]


class Node:
  def __init__(self):
    self.name = 'Untitled'
    self.children = []

  def add_childNode_(self, childNode):
    self.children.append(childNode)

  def render_commandEncoder_deltaTime_(self, commandEncoder, deltaTime):
    for child in self.children:
      child.render_commandEncoder_deltaTime_(commandEncoder, deltaTime)


class Plane(Node):
  def __init__(self, device):
    super().__init__()

    self.vertices = Vertices((Vertex(
      position=(-1.0, 1.0, 0.0), color=(1.0, 0.0, 0.0, 1.0)), Vertex(
        position=(-1.0, -1.0, 0.0), color=(0.0, 1.0, 0.0, 1.0)), Vertex(
          position=(1.0, -1.0, 0.0), color=(0.0, 0.0, 1.0, 1.0)), Vertex(
            position=(1.0, 1.0, 0.0), color=(1.0, 0.0, 1.0, 1.0)), ))
    self.indices = (ctypes.c_int16 * 6)(0, 1, 2, 2, 3, 0)
    self.constants = Constants()
    self.time = 0.0
    self.buildBuffers(device)

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
    commandEncoder.setVertexBuffer_offset_atIndex_(self.vertexBuffer, 0, 0)
    commandEncoder.setVertexBytes_length_atIndex_(
      ctypes.byref(self.constants), ctypes.sizeof(self.constants), 1)
    commandEncoder.drawIndexedPrimitives_indexCount_indexType_indexBuffer_indexBufferOffset_(
      3, self.indices.__len__(), 0, self.indexBuffer, 0)  # .triangle


class Scene(Node):
  def __init__(self, device, size):
    super().__init__()
    self.device = device
    self.size = size


class GameScene(Scene):
  def __init__(self, device, size):
    super().__init__(device, size)
    self.quad = Plane(device)
    self.add_childNode_(self.quad)


class Constants(ctypes.Structure):
  _fields_ = [('animateBy', ctypes.c_float)]


class Renderer:
  def __init__(self, device):
    self.device = device
    self.commandQueue = self.device.newCommandQueue()
    self.buildPipelineState()

  def buildPipelineState(self):
    source = shader_path.read_text('utf-8')
    library = self.device.newLibraryWithSource_options_error_(
      source, err_ptr, err_ptr)

    vertexFunction = library.newFunctionWithName_('vertex_shader')
    fragmentFunction = library.newFunctionWithName_('fragment_shader')

    rpld = ObjCClass('MTLRenderPipelineDescriptor').new()
    rpld.vertexFunction = vertexFunction
    rpld.fragmentFunction = fragmentFunction
    rpld.colorAttachments().objectAtIndexedSubscript(
      0).pixelFormat = 80  # .bgra8Unorm

    vertexDescriptor = ObjCClass('MTLVertexDescriptor').new()
    vertexDescriptor.attributes().objectAtIndexedSubscript_(0).format = 30
    vertexDescriptor.attributes().objectAtIndexedSubscript_(0).offset = 0
    vertexDescriptor.attributes().objectAtIndexedSubscript_(0).bufferIndex = 0

    vertexDescriptor.attributes().objectAtIndexedSubscript_(1).format = 31
    vertexDescriptor.attributes().objectAtIndexedSubscript_(
      1).offset = ctypes.sizeof(Position)

    vertexDescriptor.attributes().objectAtIndexedSubscript_(1).bufferIndex = 0

    vertexDescriptor.layouts().objectAtIndexedSubscript(
      0).stride = ctypes.sizeof(Vertex)

    rpld.vertexDescriptor = vertexDescriptor

    self.rps = self.device.newRenderPipelineStateWithDescriptor_error_(
      rpld, err_ptr)

  def renderer_init(self, scene):
    self.scene = scene

    # todo: MTKViewDelegate func
    def mtkView_drawableSizeWillChange_(_self, _cmd, _view, _size):
      pass

    def drawInMTKView_(_self, _cmd, _view):
      view = ObjCInstance(_view)
      drawable = view.currentDrawable()
      rpd = view.currentRenderPassDescriptor()

      deltaTime = 1 / view.preferredFramesPerSecond()

      commandBuffer = self.commandQueue.commandBuffer()
      commandEncoder = commandBuffer.renderCommandEncoderWithDescriptor_(rpd)
      commandEncoder.setRenderPipelineState_(self.rps)
      self.scene.render_commandEncoder_deltaTime_(commandEncoder, deltaTime)

      commandEncoder.endEncoding()
      commandBuffer.presentDrawable_(drawable)
      commandBuffer.commit()

    PyRenderer = create_objc_class(
      name='PyRenderer',
      methods=[drawInMTKView_, mtkView_drawableSizeWillChange_],
      protocols=['MTKViewDelegate'])
    return PyRenderer.new()


class PyMetalView:
  def __init__(self, bounds):
    self.devices = self.createSystemDefaultDevice()
    self.mtkView = ObjCClass('MTKView').alloc()
    self.view_did_load(bounds)

  def createSystemDefaultDevice(self):
    MTLCreateSystemDefaultDevice = c.MTLCreateSystemDefaultDevice
    MTLCreateSystemDefaultDevice.argtypes = []
    MTLCreateSystemDefaultDevice.restype = ctypes.c_void_p
    return ObjCInstance(MTLCreateSystemDefaultDevice())

  def view_did_load(self, bounds):
    _frame = ((0.00, 0.00), (bounds[2], bounds[3]))
    self.mtkView.initWithFrame_device_(_frame, self.devices)
    #self.mtkView.setAutoresizingMask_((1 << 1) | (1 << 4))
    self.mtkView.clearColor = wenderlichGreen
    scene = GameScene(self.devices, bounds)
    renderer = Renderer(self.devices).renderer_init(scene)
    self.mtkView.delegate = renderer


class ViewController(ui.View):
  def __init__(self, *args, **kwargs):
    ui.View.__init__(self, *args, **kwargs)
    self.bg_color = 'slategray'
    self.present(style='fullscreen', orientations=['portrait'])

    _bounds = self.bounds
    self.metal = PyMetalView(_bounds)
    self.objc_instance.addSubview_(self.metal.mtkView)


if __name__ == '__main__':
  view = ViewController()

