from pathlib import Path
import ctypes

from objc_util import c, create_objc_class, ObjCClass, ObjCInstance
import ui

import pdbg

# --- get Shader path
shader_path = Path('./challenge_Shader.metal')

# --- load objc classes
MTKView = ObjCClass('MTKView')
MTLRenderPipelineDescriptor = ObjCClass('MTLRenderPipelineDescriptor')

# --- initialize MetalDevice
MTLCreateSystemDefaultDevice = c.MTLCreateSystemDefaultDevice
MTLCreateSystemDefaultDevice.argtypes = []
MTLCreateSystemDefaultDevice.restype = ctypes.c_void_p

err_ptr = ctypes.c_void_p()


wenderlichGreen = (0.0, 0.4, 0.21, 1.0)

vertices = (ctypes.c_float * (3 * 6))(
  -1.0,  1.0, 0.0,    # v0
  -1.0, -1.0, 0.0,    # v1
   1.0, -1.0, 0.0,    # v2
   1.0, -1.0, 0.0,    # v2
   1.0,  1.0, 0.0,    # v3
  -1.0,  1.0, 0.0,    # v0
   )
'''
vertices = (ctypes.c_float * (3 * 6))(
  -0.8,  0.8, 0.0,    # v0
  -0.8, -0.8, 0.0,    # v1
   0.8, -0.8, 0.0,    # v2
   0.8, -0.8, 0.0,    # v2
   0.8,  0.8, 0.0,    # v3
  -0.8,  0.8, 0.0,    # v0
   )
'''

'''
   v0                v3
(-1, 1)--( 0, 1)--( 1, 1)
   |  \               |
   |    \             |
   |      \           |
   |        \         |
(-1, 0)  ( 0, 0)  ( 1, 0)
   |          \       |
   |            \     |
   |              \   |
   |                \ |
(-1,-1)--( 0,-1)--( 1,-1)
   v1                v2
'''


class PyMetal(ui.View):
  def __init__(self, *args, **kwargs):
    ui.View.__init__(self, *args, **kwargs)
    self.bg_color = 'slategray'
    self.view_did_load()

  def view_did_load(self):
    _device = MTLCreateSystemDefaultDevice()
    _frame = ((0.0, 0.0), (100.0, 100.0))
    devices = ObjCInstance(_device)
    mtkView = MTKView.alloc()
    mtkView.initWithFrame_device_(_frame, devices)
    mtkView.setAutoresizingMask_((1 << 1) | (1 << 4))
    mtkView.clearColor = wenderlichGreen

    renderer = self.renderer_init(devices)
    mtkView.delegate = renderer
    self.objc_instance.addSubview_(mtkView)

  def renderer_init(self, device):
    renderer = PyRenderer.alloc().init()
    renderer.commandQueue = device.newCommandQueue()

    # --- buildModel
    renderer.vertexBuffer = device.newBufferWithBytes_length_options_(
      vertices, ctypes.sizeof(vertices), 0)

    # --- buildPipelineState
    source = shader_path.read_text('utf-8')
    library = device.newLibraryWithSource_options_error_(
      source, err_ptr, err_ptr)

    vertexFunction = library.newFunctionWithName_('vertex_shader')
    fragmentFunction = library.newFunctionWithName_('fragment_shader')

    rpld = MTLRenderPipelineDescriptor.new()
    rpld.vertexFunction = vertexFunction
    rpld.fragmentFunction = fragmentFunction
    rpld.colorAttachments().objectAtIndexedSubscript(
      0).pixelFormat = 80  # .bgra8Unorm
    renderer.rps = device.newRenderPipelineStateWithDescriptor_error_(
      rpld, err_ptr)

    return renderer


# --- MTKViewDelegate
def mtkView_drawableSizeWillChange_(_self, _cmd, _view, _size):
  pass


def drawInMTKView_(_self, _cmd, _view):
  self = ObjCInstance(_self)
  view = ObjCInstance(_view)
  drawable = view.currentDrawable()
  rpd = view.currentRenderPassDescriptor()
  commandBuffer = self.commandQueue.commandBuffer()
  commandEncoder = commandBuffer.renderCommandEncoderWithDescriptor_(rpd)
  commandEncoder.setRenderPipelineState_(self.rps)
  commandEncoder.setVertexBuffer_offset_atIndex_(self.vertexBuffer, 0, 0)
  commandEncoder.drawPrimitives_vertexStart_vertexCount_(
    3, 0, vertices.__len__())  # .triangle

  commandEncoder.endEncoding()
  commandBuffer.presentDrawable_(drawable)
  commandBuffer.commit()


PyRenderer = create_objc_class(
  name='PyRenderer',
  methods=[drawInMTKView_, mtkView_drawableSizeWillChange_],
  protocols=['MTKViewDelegate'])

if __name__ == '__main__':
  view = PyMetal()
  view.present(style='fullscreen', orientations=['portrait'])

