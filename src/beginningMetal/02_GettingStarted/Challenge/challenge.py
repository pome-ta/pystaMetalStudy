import ctypes

from objc_util import c, create_objc_class, ObjCClass, ObjCInstance
import ui

wenderlichGreen = (0.0, 0.4, 0.21, 1.0)


class Renderer:
  def __init__(self, device):
    self.device = device
    self.commandQueue = self.device.newCommandQueue()

  def renderer_init(self):
    # todo: MTKViewDelegate func
    def mtkView_drawableSizeWillChange_(_self, _cmd, _view, _size):
      pass

    def drawInMTKView_(_self, _cmd, _view):
      rendererSelf = ObjCInstance(_self)
      rendererView = ObjCInstance(_view)
      drawable = rendererView.currentDrawable()
      rpd = rendererView.currentRenderPassDescriptor()
      commandBuffer = self.commandQueue.commandBuffer()
      commandEncoder = commandBuffer.renderCommandEncoderWithDescriptor_(rpd)
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

