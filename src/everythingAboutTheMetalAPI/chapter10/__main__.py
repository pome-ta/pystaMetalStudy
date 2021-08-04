import pathlib
import ctypes

from objc_util import c, create_objc_class, ObjCClass, ObjCInstance
import ui

import pdbg

shader_path = pathlib.Path('./Shaders.js')

# --- load objc classes
MTKView = ObjCClass('MTKView')

# --- initialize MetalDevice
MTLCreateSystemDefaultDevice = c.MTLCreateSystemDefaultDevice
MTLCreateSystemDefaultDevice.argtypes = []
MTLCreateSystemDefaultDevice.restype = ctypes.c_void_p

err_ptr = ctypes.c_void_p()


class MetalView(ui.View):
  def __init__(self, *args, **kwargs):
    ui.View.__init__(self, *args, **kwargs)
    self.bg_color = 'maroon'
    self.view_did_load()

  def view_did_load(self):
    mtkView = MTKView.alloc()
    _device = MTLCreateSystemDefaultDevice()
    devices = ObjCInstance(_device)

    # todo: 端末サイズにて要調整
    _uw, _uh = ui.get_window_size()
    _w = min(_uw, _uh) * 0.96
    _x = (_uw - _w) / 2
    _y = _uh / 4
    _frame = ((_x, _y), (_w, _w))
    #_frame = ((0.0, 0.0), (290.0, 290.0))

    mtkView.initWithFrame_device_(_frame, devices)
    #mtkView.setAutoresizingMask_((1 << 1) | (1 << 4))
    renderer = self.renderer_init(PyRenderer, mtkView)
    mtkView.delegate = renderer

    #mtkView.enableSetNeedsDisplay = True
    mtkView.framebufferOnly = False
    #mtkView.setNeedsDisplay()
    self.objc_instance.addSubview_(mtkView)

  def renderer_init(self, delegate, _mtkView):
    renderer = delegate.alloc().init()
    device = _mtkView.device()
    renderer.commandQueue = device.newCommandQueue()

    # --- registerShaders
    source = shader_path.read_text('utf-8')
    library = device.newLibraryWithSource_options_error_(source, err_ptr, err_ptr)
    kernel = library.newFunctionWithName_('compute')

    # maxTotalThreadsPerThreadgroup: 1024
    # threadExecutionWidth: 32
    renderer.cps = device.newComputePipelineStateWithFunction_error_(kernel, err_ptr)
    renderer.tew = renderer.cps.threadExecutionWidth()
    renderer.mttpt = renderer.cps.maxTotalThreadsPerThreadgroup()
    
    return renderer


# --- MTKViewDelegate
def drawInMTKView_(_self, _cmd, _view):
  self = ObjCInstance(_self)
  view = ObjCInstance(_view)
  

  drawable = view.currentDrawable()

  commandBuffer = self.commandQueue.commandBuffer()
  commandEncoder = commandBuffer.computeCommandEncoder()
  commandEncoder.setComputePipelineState_(self.cps)
  commandEncoder.setTexture_atIndex_(drawable.texture(), 0)

  _width = 8
  _height = 8
  _depth = 1

  threadGroupCount = (_width, _height, _depth)

  t_w = drawable.texture().width()
  t_h = drawable.texture().height()
  threadGroups = (t_w // _width, t_h // _height, 1)
  commandEncoder.dispatchThreadgroups_threadsPerThreadgroup_(threadGroups, threadGroupCount)

  commandEncoder.endEncoding()
  commandBuffer.presentDrawable_(drawable)
  commandBuffer.commit()
  #commandBuffer.waitUntilCompleted()


def mtkView_drawableSizeWillChange_(_self, _cmd, _view, _size):
  self = ObjCInstance(_self)
  view = ObjCInstance(_view)


PyRenderer = create_objc_class(
  name='PyRenderer',
  methods=[drawInMTKView_, mtkView_drawableSizeWillChange_],
  protocols=['MTKViewDelegate'])

if __name__ == '__main__':
  view = MetalView()
  view.present(style='fullscreen', orientations=['portrait'])

