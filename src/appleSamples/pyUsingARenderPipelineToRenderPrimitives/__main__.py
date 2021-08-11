from pathlib import Path
import ctypes

from objc_util import c, create_objc_class, ObjCClass, ObjCInstance

import ui
import pdbg

# --- load Shader code
shader_path = Path('./pyAAPLShaders.js')

# --- load objc classes
MTKView = ObjCClass('MTKView')
MTLRenderPipelineDescriptor = ObjCClass('MTLRenderPipelineDescriptor')


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
    '''
    # todo: 端末サイズにて要調整
    _uw, _uh = ui.get_window_size()
    _w = min(_uw, _uh) * 0.96
    _x = (_uw - _w) / 2
    _y = _uh / 4
    _frame = ((_x, _y), (_w, _w))
    '''
    
    _frame = ((0.0, 0.0), (100.0, 100.0))

    mtkView.initWithFrame_device_(_frame, devices)
    mtkView.setAutoresizingMask_((1 << 1) | (1 << 4))

    renderer = self.renderer_init(PyRenderer, mtkView)
    mtkView.delegate = renderer
    #mtkView.enableSetNeedsDisplay = True
    #mtkView.framebufferOnly = False
    #mtkView.setNeedsDisplay()
    self.objc_instance.addSubview_(mtkView)
    
  def renderer_init(self, delegate, _mtkView):
    renderer = delegate.alloc().init()
    device = _mtkView.device()
    
    source = shader_path.read_text('utf-8')
    library = device.newLibraryWithSource_options_error_(
      source, err_ptr, err_ptr)

    vertex_func = library.newFunctionWithName_('vertexShader')
    frag_func = library.newFunctionWithName_('fragmentShader')
    
    rpld = MTLRenderPipelineDescriptor.new()
    rpld.label = 'Simple Pipeline'
    rpld.vertexFunction = vertex_func
    rpld.fragmentFunction = frag_func
    
    rpld.colorAttachments().objectAtIndexedSubscript(
      0).pixelFormat = 80  # .bgra8Unorm
      
    renderer.rps = device.newRenderPipelineStateWithDescriptor_error_(
      rpld, err_ptr)

    renderer.commandQueue = device.newCommandQueue()
    
    return renderer


# --- MTKViewDelegate
def drawInMTKView_(_self, _cmd, _view):
  self = ObjCInstance(_self)
  view = ObjCInstance(_view)
  
  # --- triangleVertices
  
  
  commandBuffer = self.commandQueue.commandBuffer()
  commandBuffer.label = 'MyCommand'
  commandEncoder = commandBuffer.renderCommandEncoderWithDescriptor_(view.currentRenderPassDescriptor())
  
  pdbg.state(commandEncoder)
  
  commandEncoder.setRenderPipelineState_(self.rps)
  
  commandEncoder.endEncoding()
  commandBuffer.presentDrawable_(view.currentDrawable())
  commandBuffer.commit()
  
  


def mtkView_drawableSizeWillChange_(_self, _cmd, _view, _size):
  self = ObjCInstance(_self)
  view = ObjCInstance(_view)
  self.viewportSize_width = _size.width
  self.viewportSize_height = _size.height


PyRenderer = create_objc_class(
  name='PyRenderer',
  methods=[drawInMTKView_, mtkView_drawableSizeWillChange_],
  protocols=['MTKViewDelegate'])

if __name__ == '__main__':
  view = MetalView()
  view.present(style='fullscreen', orientations=['portrait'])

