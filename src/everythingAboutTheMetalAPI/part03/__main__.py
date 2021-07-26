import pathlib
import ctypes
from objc_util import c, create_objc_class, ObjCClass, ObjCInstance
import ui

#import pdbg

shader_path = pathlib.Path('./Shaders.metal')

# --- load objc classes
MTKView = ObjCClass('MTKView')
MTLCompileOptions = ObjCClass('MTLCompileOptions')
MTLRenderPipelineDescriptor = ObjCClass('MTLRenderPipelineDescriptor')

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
    _frame = ((0.0, 0.0), (100.0, 100.0))

    devices = ObjCInstance(_device)
    mtkView.initWithFrame_device_(_frame, devices)
    mtkView.setAutoresizingMask_((1 << 1) | (1 << 4))
    renderer = self.renderer_init(PyRenderer, mtkView)
    mtkView.delegate = renderer

    self.objc_instance.addSubview_(mtkView)

  def renderer_init(self, delegate, _mtkView):
    renderer = delegate.alloc().init()
    renderer.device = _mtkView.device()
    renderer.commandQueue = renderer.device.newCommandQueue()

    vertexData = (ctypes.c_float * 12)()
    array_vertex = [
      -1.0, -1.0, 0.0, 1.0, 1.0, -1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0
    ]
    for n, i in enumerate(array_vertex):
      vertexData[n] = i

    # xxx: 要確認
    dataSize = vertexData.__len__() * 16
    #dataSize = ctypes.sizeof(vertexData)
    renderer.vertexBuffer = renderer.device.newBufferWithBytes_length_options_(
      ctypes.byref(vertexData), dataSize, 0)

    source = shader_path.read_text('utf-8')
    library = renderer.device.newLibraryWithSource_options_error_(source, MTLCompileOptions.new(), err_ptr)

    vertex_func = library.newFunctionWithName_('vertex_func')
    frag_func = library.newFunctionWithName_('fragment_func')

    rpld = MTLRenderPipelineDescriptor.new()
    rpld.vertexFunction = vertex_func
    rpld.fragmentFunction = frag_func
    rpld.colorAttachments().objectAtIndexedSubscript(0).pixelFormat = 80  # .bgra8Unorm

    renderer.rps = renderer.device.newRenderPipelineStateWithDescriptor_error_(rpld, err_ptr)

    return renderer


# --- MTKViewDelegate
def drawInMTKView_(_self, _cmd, _view):
  self = ObjCInstance(_self)
  view = ObjCInstance(_view)
  drawable = view.currentDrawable()
  rpd = view.currentRenderPassDescriptor()
  rpd.colorAttachments().objectAtIndexedSubscript(0).clearColor = (0.0, 0.5, 0.5, 1.0)

  commandBuffer = self.commandQueue.commandBuffer()
  commandEncoder = commandBuffer.renderCommandEncoderWithDescriptor_(rpd)
  commandEncoder.setRenderPipelineState_(self.rps)
  commandEncoder.setVertexBuffer_offset_atIndex_(self.vertexBuffer, 0, 0)
  commandEncoder.drawPrimitives_vertexStart_vertexCount_instanceCount_(3, 0, 3, 1)  # .triangle
  commandEncoder.endEncoding()
  commandBuffer.presentDrawable_(drawable)
  commandBuffer.commit()


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

