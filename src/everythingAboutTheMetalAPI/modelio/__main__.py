from math import sin, cos, tan
from pathlib import Path
import ctypes

from objc_util import c, ObjCClass, ObjCInstance, nsurl
import ui


MTLCreateSystemDefaultDevice = c.MTLCreateSystemDefaultDevice
MTLCreateSystemDefaultDevice.argtypes = []
MTLCreateSystemDefaultDevice.restype = ctypes.c_void_p


class Renderer:
  def __init__(self, view):
    self.device = None
    self.commandQueue = None
    self.library = None
    self.renderPipelineState = None
    self.uniformsBuffer = None
    self.meshes = None
    self.texture = None
    self.depthStencilState = None
    # xxx: あとで事前に作る
    self.vertexDescriptor = None

    view.setClearColor_((0.5, 0.5, 0.5, 1))
    view.setColorPixelFormat_(80)

  def initializeMetalObjects(self):
    device = ObjCInstance(MTLCreateSystemDefaultDevice())
    commandQueue = device.newCommandQueue()


class MTKView(ui.View):
  # xxx: frame size
  def __init__(self, *args, **kwargs):
    ui.View.__init__(self, *args, **kwargs)
    self.bg_color = 'slategra'

    _frame = ((0.0, 0.0), (300.0, 600.0))
    self.mtkView = ObjCClass('MTKView').alloc()
    self.mtkView.initWithFrame_(_frame)
    renderer = Renderer(self.mtkView)
    self.objc_instance.addSubview_(self.mtkView)


if __name__ == '__main__':
  view = MTKView()
  view.present(style='fullscreen', orientations=['portrait'])

