import pathlib
import ctypes
from objc_util import c, create_objc_class, ObjCClass, ObjCInstance
import ui

import pdbg


shader_path = pathlib.Path('./Shaders.metal')

# --- load objc classes
MTKView = ObjCClass('MTKView')
MTLRenderPipelineDescriptor = ObjCClass('MTLRenderPipelineDescriptor')
MTLCompileOptions = ObjCClass('MTLCompileOptions')

# --- initialize MetalDevice
MTLCreateSystemDefaultDevice = c.MTLCreateSystemDefaultDevice
MTLCreateSystemDefaultDevice.argtypes = []
MTLCreateSystemDefaultDevice.restype = ctypes.c_void_p

err_ptr = ctypes.c_void_p()


# --- set Structures
class Position(ctypes.Structure):
  _fields_ = [('x', ctypes.c_float), ('y', ctypes.c_float), ('z', ctypes.c_float)]


class Vertex(ctypes.Structure):
  _fields_ = [('pos', Position)]


class PyVertex(ctypes.Structure):
  _fields_ = [('x', Vertex), ('y', Vertex), ('z', Vertex), ('w', Vertex)]

'''
class Indices(ctypes.Structure):
  _fields_ = [
    ('a', ctypes.c_int16),
    ('b', ctypes.c_int16),
    ('c', ctypes.c_int16),
    ('d', ctypes.c_int16),
    ('e', ctypes.c_int16),
    ('f', ctypes.c_int16),
  ]
'''

Indices = (ctypes.c_int16 * 6)()
ptr_indices = [0, 1, 2, 1, 2, 3]
for n, i in enumerate(ptr_indices):
  Indices[n] = i


'''
class PyIndices(ctypes.Structure):
  _fields_ = [('a', ctypes.c_void_p)]
'''

vertices = PyVertex(
  Vertex(Position(-1.0, -1.0, 0.0)),
  Vertex(Position(1.0, -1.0, 0.0)),
  Vertex(Position(-1.0, 1.0, 0.0)), Vertex(Position(1.0, 1.0, 0.0)))

#indices = PyIndices(Indices(0, 1, 2, 1, 2, 3))
#indices = Indices(0, 1, 2, 1, 2, 3)
indices = Indices

#print(ctypes.sizeof(indices))

float2 = ctypes.c_float * 2


class Uniforms(ctypes.Structure):
  _fields_ = [('time', ctypes.c_float), ('aspectRatio', ctypes.c_float), ('touch', float2)]


class View(ui.View):
  def __init__(self, *args, **kwargs):
    ui.View.__init__(self, *args, **kwargs)
    self.bg_color = 'maroon'
    self.view_did_load()

  def view_did_load(self):
    mtkView = MTKView.alloc()
    _device = MTLCreateSystemDefaultDevice()

    defaultDevice = ObjCInstance(_device)
    mtkView.initWithFrame_device_(((0, 0), (100, 100)), defaultDevice)
    mtkView.setAutoresizingMask_((1 << 1) | (1 << 4))
    mtkView.framebufferOnly = True
    renderer = self.renderer_init(PyRenderer, mtkView)
    mtkView.delegate = renderer

    self.objc_instance.addSubview_(mtkView)

  def renderer_init(self, delegate, _mtkView):
    renderer = delegate.alloc().init()
    renderer.device = _mtkView.device()
    renderer.commandQueue = renderer.device.newCommandQueue()

    # --- buildPipeline
    source = shader_path.read_text('utf-8')
    library = renderer.device.newLibraryWithSource_options_error_(source, MTLCompileOptions.new(), err_ptr)

    vertexProgram = library.newFunctionWithName_('vertexDay1')

    fragmentProgram = library.newFunctionWithName_('fragmentDay1')

    pipelineDescriptor = MTLRenderPipelineDescriptor.alloc().init()
    pipelineDescriptor.vertexFunction = vertexProgram
    pipelineDescriptor.fragmentFunction = fragmentProgram
    pipelineDescriptor.colorAttachments().objectAtIndexedSubscript(0).pixelFormat = 80  # .bgra8Unorm

    renderer.pipelineState = renderer.device.newRenderPipelineStateWithDescriptor_error_(pipelineDescriptor, err_ptr)

    # --- buildBuffer
    renderer.vertexBuffer = renderer.device.newBufferWithBytes_length_options_(ctypes.byref(vertices), ctypes.sizeof(vertices), 0)
    

    renderer.indexBuffer = renderer.device.newBufferWithBytes_length_options_(indices, ctypes.sizeof(indices), 0)
    

    renderer.preferredFramesTime = 1.0 / _mtkView.preferredFramesPerSecond()

    renderer.uniforms = Uniforms()
    size = _mtkView.frame().size
    renderer.uniforms.aspectRatio = size.width / size.height

    return renderer


# --- MTKViewDelegate
def drawInMTKView_(_self, _cmd, _view):
  self = ObjCInstance(_self)
  view = ObjCInstance(_view)

  self.uniforms.time += self.preferredFramesTime

  drawable = view.currentDrawable()
  renderPassDescriptor = view.currentRenderPassDescriptor()

  commandBuffer = self.commandQueue.commandBuffer()
  renderEncoder = commandBuffer.renderCommandEncoderWithDescriptor_(renderPassDescriptor)
  renderEncoder.setRenderPipelineState_(self.pipelineState)
  renderEncoder.setVertexBuffer_offset_atIndex_(self.vertexBuffer, 0, 0)

  renderEncoder.setVertexBytes_length_atIndex_(ctypes.byref(self.uniforms), ctypes.sizeof(self.uniforms), 1)
  

  renderEncoder.drawIndexedPrimitives_indexCount_indexType_indexBuffer_indexBufferOffset_(2, 16, 0, self.indexBuffer, 0)
  renderEncoder.endEncoding()
  commandBuffer.presentDrawable_(drawable)
  commandBuffer.commit()


def mtkView_drawableSizeWillChange_(_self, _cmd, _view, _size):
  self = ObjCInstance(_self)
  view = ObjCInstance(_view)
  size = view.frame().size
  self.uniforms.aspectRatio = size.width / size.height
  


PyRenderer = create_objc_class(
  name='PyRenderer',
  methods=[drawInMTKView_, mtkView_drawableSizeWillChange_],
  protocols=['MTKViewDelegate'])

if __name__ == '__main__':
  view = View()
  view.present(style='fullscreen', orientations=['portrait'])

