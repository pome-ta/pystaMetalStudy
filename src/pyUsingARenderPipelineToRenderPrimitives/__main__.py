from pathlib import Path
import ctypes
from objc_util import c, create_objc_class, ObjCClass, ObjCInstance, ns, sel
import ui
import pdbg

#shader_path = Path('./AAPLShaders.metal')
#shader_path = Path('./Shaders.metal')
#shader_path = Path('./mShaders.metal')
shader_path = Path('./main.metal')

# --- load objc classes
MTKView = ObjCClass('MTKView')
MTLCompileOptions = ObjCClass('MTLCompileOptions')
MTLRenderPipelineDescriptor = ObjCClass('MTLRenderPipelineDescriptor')

# --- objc definition
err_ptr = ctypes.c_void_p()

MTLCreateSystemDefaultDevice = c.MTLCreateSystemDefaultDevice

MTLCreateSystemDefaultDevice.argtypes = []
MTLCreateSystemDefaultDevice.restype = ctypes.c_void_p

MTLPrimitiveTypeTriangle = 3
AAPLVertexInputIndexVertices     = 0
AAPLVertexInputIndexViewportSize = 1


# --- delegate setup
def drawInMTKView_(_self, _cmd, _view):
  self = ObjCInstance(_self)
  view = ObjCInstance(_view)
  
  triangleVertices = ns(
    (  # 2D positions,    RGBA colors
      ( 250.0, -250.0), (1.0, 0.0, 0.0, 1.0),
      (-250.0, -250.0), (0.0, 1.0, 0.0, 1.0),
      (   0.0,  250.0), (0.0, 0.0, 1.0, 1.0),
    )
  )

  commandBuffer = self.commandQueue.commandBuffer()
  commandBuffer.label = 'MyCommand'

  renderPassDescriptor = view.currentRenderPassDescriptor()

  if renderPassDescriptor != None:
    renderEncoder = commandBuffer.renderCommandEncoderWithDescriptor_(
      renderPassDescriptor)

    renderEncoder.label = 'MyRenderEncoder'
    
    renderEncoder.setViewport_((0.0, 0.0, self.viewportSize.x, self.viewportSize.y, 0.0, 1.0))
    
    renderEncoder.setRenderPipelineState_(self.pipelineState)
    renderEncoder.setVertexBytes_length_atIndex_(ctypes.byref(triangleVertices), ctypes.sizeof(triangleVertices), AAPLVertexInputIndexVertices)
    
    renderEncoder.setVertexBytes_length_atIndex_(ctypes.byref(self.viewportSize), ctypes.sizeof(self.viewportSize), AAPLVertexInputIndexViewportSize)
    
    renderEncoder.drawPrimitives_vertexStart_vertexCount_(MTLPrimitiveTypeTriangle, 0, 3)
    renderEncoder.endEncoding()
    commandBuffer.presentDrawable_(view.currentDrawable())

  commandBuffer.commit()


def mtkView_drawableSizeWillChange_(_self, _cmd, _view, _size):
  self = ObjCInstance(_self)
  self.viewportSize.x = _size.width
  self.viewportSize.y = _size.height
  print(_size.width, _size.height)
  print('mtkView_drawableSizeWillChange_')


AAPLRenderer = create_objc_class(
  name='AAPLRenderer',
  methods=[drawInMTKView_, mtkView_drawableSizeWillChange_],
  protocols=['MTKViewDelegate'])


class View(ui.View):
  def __init__(self, *args, **kwargs):
    ui.View.__init__(self, *args, **kwargs)
    self.instance = ObjCInstance(self)
    self.bg_color = 'maroon'
    self.view_did_load()

  def view_did_load(self):
    _view = MTKView.alloc()
    _view.enableSetNeedsDisplay = True
    _view.initWithFrame_device_(((0, 0), (32, 32)),
                                ObjCInstance(MTLCreateSystemDefaultDevice()))
    _view.setAutoresizingMask_((1 << 1) | (1 << 4))
    _view.clearColor = (0.0, 0.5, 1.0, 1.0)
    _renderer = self.renderer_init(AAPLRenderer, _view)
    _view.delegate = _renderer

    self.instance.addSubview_(_view)

  # todo: initWithMetalKitView:
  def renderer_init(self, delegate_cls, mtkView):
    renderer = delegate_cls.alloc().init()
    renderer.device = mtkView.device()

    shader_sauce = shader_path.read_text('utf-8')
    defaultLibrary = renderer.device.newLibraryWithSource_options_error_(
      shader_sauce, MTLCompileOptions.new(), err_ptr)

    vertexFunction = defaultLibrary.newFunctionWithName_('vertexShader')
    fragmentFunction = defaultLibrary.newFunctionWithName_('fragmentShader')

    pipelineStateDescriptor = MTLRenderPipelineDescriptor.alloc().init()

    pipelineStateDescriptor.label = 'Simple Pipeline'

    pipelineStateDescriptor.vertexFunction = vertexFunction
    pipelineStateDescriptor.fragmentFunction = fragmentFunction

    pipelineStateDescriptor.colorAttachments().objectAtIndexedSubscript_(
      0).pixelFormat = mtkView.colorPixelFormat()

    renderer.pipelineState = renderer.device.newRenderPipelineStateWithDescriptor_error_(
      pipelineStateDescriptor, err_ptr)

    renderer.commandQueue = renderer.device.newCommandQueue()
    
    renderer.viewportSize.x = 0
    renderer.viewportSize.y = 0
    
    return renderer


if __name__ == '__main__':
  view = View()
  view.present(style='fullscreen', orientations=['portrait'])

