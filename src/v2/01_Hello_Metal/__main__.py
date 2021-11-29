import ctypes

from objc_util import c, ObjCClass, ObjCInstance
import ui

import pdbg

MTLCreateSystemDefaultDevice = c.MTLCreateSystemDefaultDevice
MTLCreateSystemDefaultDevice.argtypes = []
MTLCreateSystemDefaultDevice.restype = ctypes.c_void_p

device = ObjCInstance(MTLCreateSystemDefaultDevice())

MTKView = ObjCClass('MTKView')
frame = ((0.0, 0.0), (300.0, 300.0))
view = MTKView.alloc().initWithFrame_device_(frame, device)
view.clearColor = (1.0, 1.0, 1.0)

MTKMeshBufferAllocator = ObjCClass('MTKMeshBufferAllocator')

allocator = MTKMeshBufferAllocator.new().initWithDevice_(device)

MDLMesh = ObjCClass('MDLMesh')
mdlMesh = MDLMesh.new()




class ViewController(ui.View):
  def __init__(self, *args, **kwargs):
    ui.View.__init__(self, *args, **kwargs)
    self.bg_color = 'slategray'


if __name__ == '__main__':
  view = ViewController()
  view.present(style='fullscreen')

