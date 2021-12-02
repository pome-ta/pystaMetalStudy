import ctypes

from objc_util import c, ObjCClass, ObjCInstance, load_framework
import ui

import pdbg


load_framework('')

err_ptr = ctypes.c_void_p()

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
#mdlMesh = MDLMesh.new()

commandQueue = device.newCommandQueue()

shader = '''
#include <metal_stdlib>
using namespace metal;
struct VertexIn {
  float4 position [[ attribute(0) ]];
};
vertex float4 vertex_main(const VertexIn vertex_in [[ stage_in ]]) {
  return vertex_in.position;
}
fragment float4 fragment_main() {
  return float4(1, 0, 0, 1);
}
'''


library = device.newLibraryWithSource_options_error_(shader, err_ptr, err_ptr)

vertexFunction = library.newFunctionWithName_('vertex_main')
fragmentFunction = library.newFunctionWithName_('fragment_main')

MTLRenderPipelineDescriptor = ObjCClass('MTLRenderPipelineDescriptor')

pipelineDescriptor = MTLRenderPipelineDescriptor.new()

# MTLPixelFormatBGRA8Unorm
pipelineDescriptor.colorAttachments().objectAtIndexedSubscript_(0).pixelFormat = 80

pipelineDescriptor.vertexFunction = vertexFunction
pipelineDescriptor.fragmentFunction = fragmentFunction



class ViewController(ui.View):
  def __init__(self, *args, **kwargs):
    ui.View.__init__(self, *args, **kwargs)
    self.bg_color = 'slategray'


if __name__ == '__main__':
  view = ViewController()
  view.present(style='fullscreen')

