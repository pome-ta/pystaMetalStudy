from pathlib import Path
from math import sin
import ctypes

from objc_util import c, create_objc_class, ObjCClass, ObjCInstance
import ui

# --- get Shader path
shader_path = Path('./final_Shader.metal')

wenderlichGreen = (0.0, 0.4, 0.21, 1.0)
err_ptr = ctypes.c_void_p()


class Constants(ctypes.Structure):
  _fields_ = [('animateBy', ctypes.c_float)]


class Renderer:
  def __init__(self, device):
    self.device = device
    self.commandQueue = self.device.newCommandQueue()
    
    self.vertices = (ctypes.c_float * 12)(
      -1.0,  1.0, 0.0,    # v0
      -1.0, -1.0, 0.0,    # v1
       1.0, -1.0, 0.0,    # v2
       1.0,  1.0, 0.0,)   # v3
    self.indices = (ctypes.c_int16 * 6)(0, 1, 2, 2, 3, 0)
    self.constants = Constants()
    self.time = 0.0

    self.buildModel()
    self.buildPipelineState()

  def buildModel(self):
    self.vertexBuffer = self.device.newBufferWithBytes_length_options_(
      self.vertices, self.vertices.__len__() * ctypes.sizeof(self.vertices), 0)
    self.indexBuffer = self.device.newBufferWithBytes_length_options_(
      self.indices, self.indices.__len__() * ctypes.sizeof(self.indices), 0)

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
    self.rps = self.device.newRenderPipelineStateWithDescriptor_error_(
      rpld, err_ptr)

  def renderer_init(self):

    # todo: MTKViewDelegate func
    def mtkView_drawableSizeWillChange_(_self, _cmd, _view, _size):
      pass

    def drawInMTKView_(_self, _cmd, _view):
      view = ObjCInstance(_view)
      drawable = view.currentDrawable()
      rpd = view.currentRenderPassDescriptor()

      self.time += 1 / view.preferredFramesPerSecond()
      animateBy = abs(sin(self.time) / 2 + 0.5)
      self.constants.animateBy = animateBy

      commandBuffer = self.commandQueue.commandBuffer()
      commandEncoder = commandBuffer.renderCommandEncoderWithDescriptor_(rpd)
      commandEncoder.setRenderPipelineState_(self.rps)
      commandEncoder.setVertexBuffer_offset_atIndex_(self.vertexBuffer, 0, 0)
      commandEncoder.setVertexBytes_length_atIndex_(
        ctypes.byref(self.constants), ctypes.sizeof(self.constants), 1)
      commandEncoder.drawIndexedPrimitives_indexCount_indexType_indexBuffer_indexBufferOffset_(
        3, self.indices.__len__(), 0, self.indexBuffer, 0)  # .triangle

      commandEncoder.endEncoding()
      commandBuffer.presentDrawable_(drawable)
      commandBuffer.commit()

    PyRenderer = create_objc_class(
      name='PyRenderer',
      methods=[drawInMTKView_, mtkView_drawableSizeWillChange_],
      protocols=['MTKViewDelegate'])
    return PyRenderer.new()


class PyMetalView:
  def __init__(self):
    self.devices = self.createSystemDefaultDevice()
    self.mtkView = ObjCClass('MTKView').alloc()
    self.view_did_load()

  def createSystemDefaultDevice(self):
    MTLCreateSystemDefaultDevice = c.MTLCreateSystemDefaultDevice
    MTLCreateSystemDefaultDevice.argtypes = []
    MTLCreateSystemDefaultDevice.restype = ctypes.c_void_p
    return ObjCInstance(MTLCreateSystemDefaultDevice())

  def view_did_load(self):
    _frame = ((0.0, 0.0), (100.0, 100.0))
    self.mtkView.initWithFrame_device_(_frame, self.devices)
    self.mtkView.setAutoresizingMask_((1 << 1) | (1 << 4))
    self.mtkView.clearColor = wenderlichGreen
    renderer = Renderer(self.devices).renderer_init()
    self.mtkView.delegate = renderer


class ViewController(ui.View):
  def __init__(self, *args, **kwargs):
    ui.View.__init__(self, *args, **kwargs)
    self.bg_color = 'slategray'
    self.metal = PyMetalView()
    self.objc_instance.addSubview_(self.metal.mtkView)


if __name__ == '__main__':
  view = ViewController()
  view.present(style='fullscreen', orientations=['portrait'])

