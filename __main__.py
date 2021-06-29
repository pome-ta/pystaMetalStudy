import pathlib
import ctypes
from objc_util import c, ObjCClass, ObjCInstance, on_main_thread, ns
import ui
import pdbg

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


vertexData = [
   0.0,  1.0, 0.0,
  -1.0, -1.0, 0.0,
   1.0, -1.0, 0.0
 ]
 
shader_path = pathlib.Path('./Shaders.metal')


err_ptr = ctypes.c_void_p()


class View(ui.View):
  def __init__(self, *args, **kwargs):
    ui.View.__init__(self, *args, **kwargs)
    self.bg_color = 'maroon'
    self.instance = ObjCInstance(self)
    self.view_did_load()
  
  @on_main_thread
  def view_did_load(self):
    
    device = ObjCInstance(MTLCreateSystemDefaultDevice())
    metalLayer = CAMetalLayer.new()
    metalLayer.device = device
    metalLayer.pixelFormat = bgra8Unorm
    metalLayer.framebufferOnly = True
    metalLayer.frame = self.instance.layer().frame()
    self.instance.layer().addSublayer_(metalLayer)
    
    # xxx: size の取り方 - `float` だから16にしてる
    dataSize = len(vertexData) * 16
    vertexBuffer = device.newBufferWithBytes_length_options_(ns(vertexData), dataSize, 0)
    
    source = shader_path.read_text('utf-8')
    defaultLibrary = device.newLibraryWithSource_options_error_(source, MTLCompileOptions.new(), err_ptr)
    
    fragmentProgram = defaultLibrary.newFunctionWithName_('basic_fragment')
    vertexProgram = defaultLibrary.newFunctionWithName_('basic_vertex')
    
    pipelineStateDescriptor = MTLRenderPipelineDescriptor.new()
    pipelineStateDescriptor.vertexFunction = vertexProgram
    pipelineStateDescriptor.fragmentFunction = fragmentProgram
    
    pipelineStateDescriptor.colorAttachments().objectAtIndexedSubscript(0).pixelFormat = bgra8Unorm
    
    device.newRenderPipelineStateWithDescriptor_error_(pipelineStateDescriptor, err_ptr)
    
    
    commandQueue = device.newCommandQueue()
    #MTLRenderPassDescriptor
    
  def render(self):
    pass
    
    
    
    
    #pdbg.state(device)
    
    
    
    
    
    

if __name__ == '__main__':
  view = View()
  view.present(style='fullscreen', orientations=['portrait'])

