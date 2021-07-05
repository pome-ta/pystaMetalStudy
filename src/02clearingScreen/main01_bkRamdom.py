import ctypes
from objc_util import c, create_objc_class, ObjCClass, ObjCInstance
import ui
#import pdbg

from random import random

MTKView = ObjCClass('MTKView')

MTLCreateSystemDefaultDevice = c.MTLCreateSystemDefaultDevice

MTLCreateSystemDefaultDevice.argtypes = []
MTLCreateSystemDefaultDevice.restype = ctypes.c_void_p


def drawInMTKView_(_self, _cmd, _view):
  d_self = ObjCInstance(_self)
  view = ObjCInstance(_view)

  commandBuffer = d_self.commandQueue.commandBuffer()
  renderPassDescriptor = view.currentRenderPassDescriptor()

  renderPassDescriptor.colorAttachments().objectAtIndexedSubscript(
    0).clearColor = (random(), random(), random(), 1.0)

  renderEncoder = commandBuffer.renderCommandEncoderWithDescriptor_(
    renderPassDescriptor)
  renderEncoder.endEncoding()
  commandBuffer.presentDrawable_(view.currentDrawable())
  commandBuffer.commit()


def mtkView_drawableSizeWillChange_(_self, _cmd, _view, _size):
  print('drawableSizeWillChange')


PyRenderer = create_objc_class(
  name='PyRenderer',
  methods=[drawInMTKView_, mtkView_drawableSizeWillChange_],
  protocols=['MTKViewDelegate'])


class View(ui.View):
  def __init__(self, *args, **kwargs):
    ui.View.__init__(self, *args, **kwargs)
    self.mtkView = MTKView.alloc()
    self.view_did_load()
    self.bg_color = 'maroon'
    instance = ObjCInstance(self)
    instance.addSubview_(self.mtkView)

  def view_did_load(self):
    _device = MTLCreateSystemDefaultDevice()
    defaultDevice = ObjCInstance(_device)
    frame = ((0, 0), (100, 100))
    self.mtkView.initWithFrame_device_(frame, defaultDevice)
    self.mtkView.setAutoresizingMask_((1 << 1) | (1 << 4))
    self.mtkView.setClearColor_((0.0, 1.0, 1.0, 1.0))

    renderer = PyRenderer.new()
    renderer.commandQueue = self.mtkView.device().newCommandQueue()
    self.mtkView.setDelegate_(renderer)


if __name__ == '__main__':
  view = View()
  view.present(style='fullscreen', orientations=['portrait'])

