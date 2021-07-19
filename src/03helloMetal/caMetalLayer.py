from pathlib import Path
import ctypes
from objc_util import c, create_objc_class, ObjCClass, ObjCInstance, ns, on_main_thread
import ui
import pdbg

from random import random

from pprint import pprint

shader_path = Path('./Shaders.metal')

CAMetalLayer = ObjCClass('CAMetalLayer')
MTLCompileOptions = ObjCClass('MTLCompileOptions')
MTLRenderPipelineDescriptor = ObjCClass('MTLRenderPipelineDescriptor')
MTLRenderPassDescriptor = ObjCClass('MTLRenderPassDescriptor')

MTLCreateSystemDefaultDevice = c.MTLCreateSystemDefaultDevice

MTLCreateSystemDefaultDevice.argtypes = []
MTLCreateSystemDefaultDevice.restype = ctypes.c_void_p

float_3 = ctypes.c_float * 3
class Vertex(ctypes.Structure):
  _fields_ = [('ax', float_3), ('ay', float_3), ('az', float_3)]


vertexData = Vertex((0.0, 1.0, 0.0), (-1.0, -1.0, 0.0), (1.0, -1.0, 0.0))

MTLCPUCacheModeDefaultCache = 0
MTLResourceCPUCacheModeShift = 0

MTLResourceCPUCacheModeDefaultCache = MTLCPUCacheModeDefaultCache << MTLResourceCPUCacheModeShift


err_ptr = ctypes.c_void_p()


class View(ui.View):
  def __init__(self, *args, **kwargs):
    #ui.View.__init__(self, *args, **kwargs)
    interval = 8
    self.update_interval = 1 / interval
    self.bg_color = 'maroon'
    self.view_did_load()
    #self.render()

  #@on_main_thread
  def view_did_load(self):
    _device = MTLCreateSystemDefaultDevice()
    device = ObjCInstance(_device)
    self.metalLayer = CAMetalLayer.alloc().init()
    self.metalLayer.device = device
    self.metalLayer.pixelFormat = 80  # .bgra8Unorm
    self.metalLayer.framebufferOnly = True

    self.metalLayer.frame = self.objc_instance.layer().frame()
    self.objc_instance.layer().addSublayer_(self.metalLayer)

    dataSize = 9 * 16#pyvertexData.__sizeof__()
    self.vertexBuffer = device.newBufferWithBytes_length_options_(
      ctypes.byref(vertexData), dataSize, MTLResourceCPUCacheModeDefaultCache)

    source = shader_path.read_text('utf-8')
    defaultLibrary = device.newLibraryWithSource_options_error_(
      source, MTLCompileOptions.new(), err_ptr)

    fragmentProgram = defaultLibrary.newFunctionWithName_('basic_fragment')
    vertexProgram = defaultLibrary.newFunctionWithName_('basic_vertex')

    pipelineStateDescriptor = MTLRenderPipelineDescriptor.alloc().init()

    pipelineStateDescriptor.vertexFunction = vertexProgram
    pipelineStateDescriptor.fragmentFunction = fragmentProgram

    pipelineStateDescriptor.colorAttachments().objectAtIndexedSubscript(
      0).pixelFormat = 80

    self.pipelineState = device.newRenderPipelineStateWithDescriptor_error_(
      pipelineStateDescriptor, err_ptr)

    self.commandQueue = device.newCommandQueue()
    self.render()

  #@on_main_thread
  def render(self):
    drawable = self.metalLayer.nextDrawable()
    renderPassDescriptor = MTLRenderPassDescriptor.alloc().init()

    renderPassDescriptor.colorAttachments().objectAtIndexedSubscript(
      0).texture = drawable.texture()
    renderPassDescriptor.colorAttachments().objectAtIndexedSubscript(
      0).loadAction = 2  # MTLLoadAction.clear

    #(random(), random(), random(), 1.0)
    #(0.0, 104.0 / 255.0, 55.0 / 255.0, 1.0)
    renderPassDescriptor.colorAttachments().objectAtIndexedSubscript(
      0).clearColor = (random(), random(), random(), 1.0)

    commandBuffer = self.commandQueue.commandBuffer()
    renderEncoder = commandBuffer.renderCommandEncoderWithDescriptor_(
      renderPassDescriptor)

    renderEncoder.setRenderPipelineState_(self.pipelineState)
    renderEncoder.setVertexBuffer_offset_atIndex_(self.vertexBuffer, 0, 0)
    renderEncoder.drawPrimitives_vertexStart_vertexCount_instanceCount_(
      4, 0, 3, 1)

    renderEncoder.endEncoding()

    commandBuffer.presentDrawable(drawable)
    commandBuffer.commit()

  def update(self):
    self.render()


if __name__ == '__main__':
  view = View()
  view.present(style='fullscreen', orientations=['portrait'])
  #view.present()


