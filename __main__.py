import pathlib
import ctypes
from objc_util import c, ObjCClass, ObjCInstance, create_objc_class, ns, load_framework
import ui
import pdbg


#load_framework('Metal')


MTLCreateSystemDefaultDevice = c.MTLCreateSystemDefaultDevice

MTLCreateSystemDefaultDevice.argtypes = []
MTLCreateSystemDefaultDevice.restype = ctypes.c_void_p

MTKView = ObjCClass('MTKView')
CAMetalLayer = ObjCClass('CAMetalLayer')
MTLCompileOptions = ObjCClass('MTLCompileOptions')
MTLRenderPipelineDescriptor = ObjCClass('MTLRenderPipelineDescriptor')
MTLRenderPassDescriptor = ObjCClass('MTLRenderPassDescriptor')

#pdbg.state(MTLRenderPassDescriptor)

bgra8Unorm = 80

vertexData = [0.0, 1.0, 0.0, -1.0, -1.0, 0.0, 1.0, -1.0, 0.0]

shader_path = pathlib.Path('./Shaders.metal')

err_ptr = ctypes.c_void_p()

'''
def mtkView_drawableSizeWillChange(_self, _cmd, view, size):
  pass

def drawInMTKView_(_self, _cmd, view):
  mView = ObjCInstance(view)
  #drawable 
  #pass

myMTKViewDelegate = create_objc_class(
  name='myMTKViewDelegate',
  methods=[mtkView_drawableSizeWillChange, drawInMTKView_],
  protocols=['MTKViewDelegate'])

'''


class View(ui.View):
  def __init__(self, *args, **kwargs):
    ui.View.__init__(self, *args, **kwargs)
    self.bg_color = 'maroon'
    self.update_interval = 1 / 1
    self.instance = ObjCInstance(self)
    self.view_did_load()

  def view_did_load(self):

    device = ObjCInstance(MTLCreateSystemDefaultDevice())
    metalLayer = CAMetalLayer.new()
    mtkView = MTKView.alloc()
    #pdbg.state(mtkView)
    mtkView.initWithFrame_device_(((0, 0), (100, 100)), device)
    mtkView.setAutoresizingMask_((1 << 1) | (1 << 4))
    mtkView.setColorPixelFormat_(bgra8Unorm)
    mtkView.setFramebufferOnly_(True)
    #self.instance.addSubview_(mtkView)
    
    # xxx: size の取り方 - `float` だから16にしてる
    dataSize = len(vertexData) * 16
    vertexBuffer = device.newBufferWithBytes_length_options_(
      ns(vertexData), dataSize, 0)

    source = shader_path.read_text('utf-8')
    defaultLibrary = device.newLibraryWithSource_options_error_(
      source, MTLCompileOptions.new(), err_ptr)

    fragmentProgram = defaultLibrary.newFunctionWithName_('basic_fragment')
    vertexProgram = defaultLibrary.newFunctionWithName_('basic_vertex')

    pipelineStateDescriptor = MTLRenderPipelineDescriptor.new()
    pipelineStateDescriptor.vertexFunction = vertexProgram
    pipelineStateDescriptor.fragmentFunction = fragmentProgram

    pipelineStateDescriptor.colorAttachments().objectAtIndexedSubscript(
      0).pixelFormat = bgra8Unorm

    device.newRenderPipelineStateWithDescriptor_error_(pipelineStateDescriptor,
                                                       err_ptr)

    commandQueue = device.newCommandQueue()
    #MTLRenderPassDescriptor

  def render(self):
    pass

    #pdbg.state(device)


if __name__ == '__main__':
  view = View()
  view.present(style='fullscreen', orientations=['portrait'])

