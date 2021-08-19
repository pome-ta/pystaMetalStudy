from pathlib import Path
from math import sin
import ctypes

from objc_util import c, create_objc_class, ObjCClass, ObjCInstance
import ui

import pdbg

# --- get Shader path
#shader_path = Path('./final_Shader.metal')
shader_path = Path('./noMotion_final_Shader.metal')

# --- load objc classes
MTKView = ObjCClass('MTKView')
MTLRenderPipelineDescriptor = ObjCClass('MTLRenderPipelineDescriptor')

# --- initialize MetalDevice
MTLCreateSystemDefaultDevice = c.MTLCreateSystemDefaultDevice
MTLCreateSystemDefaultDevice.argtypes = []
MTLCreateSystemDefaultDevice.restype = ctypes.c_void_p

err_ptr = ctypes.c_void_p()

wenderlichGreen = (0.0, 0.4, 0.21, 1.0)
'''
vertices = (ctypes.c_float * 12)(
  -1.0,  1.0, 0.0,    # v0
  -1.0, -1.0, 0.0,    # v1
   1.0, -1.0, 0.0,    # v2
   1.0,  1.0, 0.0,)   # v3
'''
vertices = (ctypes.c_float * 12)(
  -0.8,  0.8, 0.0,    # v0
  -0.8, -0.8, 0.0,    # v1
   0.8, -0.8, 0.0,    # v2
   0.8,  0.8, 0.0,)   # v3


indices = (ctypes.c_int16 * 6)(0, 1, 2, 2, 3, 0)

'''
class Constants(ctypes.Structure):
  _fields_ = [('animateBy', ctypes.c_float)]


constants = Constants()
animateBy = (ctypes.c_float)(0.0)
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

    #renderer.time = 0.0

    # --- buildModel
    renderer.vertexBuffer = device.newBufferWithBytes_length_options_(
      vertices, vertices.__len__() * ctypes.sizeof(vertices), 0)

    renderer.indexBuffer = device.newBufferWithBytes_length_options_(
      indices, indices.__len__() * ctypes.sizeof(indices), 0)

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

  #self.time += 1 / view.preferredFramesPerSecond()
  #animateBy.value = abs(sin(self.time) / 2 + 0.5)
  #constants.animateBy = animateBy

  commandBuffer = self.commandQueue.commandBuffer()
  commandEncoder = commandBuffer.renderCommandEncoderWithDescriptor_(rpd)
  commandEncoder.setRenderPipelineState_(self.rps)
  commandEncoder.setVertexBuffer_offset_atIndex_(self.vertexBuffer, 0, 0)
  '''
  commandEncoder.setVertexBytes_length_atIndex_(
    ctypes.byref(constants), ctypes.sizeof(constants), 1)
  '''
  commandEncoder.drawIndexedPrimitives_indexCount_indexType_indexBuffer_indexBufferOffset_(
    3, indices.__len__(), 0, self.indexBuffer, 0)

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

