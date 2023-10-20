import ctypes

from objc_util import c, ObjCClass, ObjCInstance, load_framework, ns, sel, create_objc_class
import ui

import pdbg


load_framework('SceneKit')
load_framework('ModelIO')

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

extent = (ctypes.c_float * 3)(0.75, 0.75, 0.75)
segments = (ctypes.c_uint32 * 2)(100, 100)


SCNBox = ObjCClass('SCNBox')
box = SCNBox.box()
box.width = 1
box.height = 1
box.length = 1
#pdbg.state(box)


#pdbg.state(MDLMesh)
#mdlMesh = MDLMesh.new().initSphereWithExtent_segments_inwardNormals_geometryType_allocator_((0.75, 0.75, 0.75), (100, 100),0,2, allocator)
#mdlMesh = ObjCClass('MDLMesh').newBoxWithDimensions_segments_geometryType_inwardNormals_allocator_(extent, segments, 0, 2, allocator)

mdlMesh = MDLMesh.meshWithSCNGeometry_bufferAllocator_(box, allocator)


MTKMesh = ObjCClass('MTKMesh')


mesh = MTKMesh.alloc().initWithMesh_device_error_(mdlMesh, device, err_ptr)
#pdbg.state(mesh)

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
pipelineDescriptor.colorAttachments().objectAtIndexedSubscript_(
  0).pixelFormat = 80

pipelineDescriptor.vertexFunction = vertexFunction
pipelineDescriptor.fragmentFunction = fragmentFunction

pipelineState = device.newRenderPipelineStateWithDescriptor_error_(
  pipelineDescriptor, err_ptr)

commandBuffer = commandQueue.commandBuffer()

renderPassDescriptor = view.currentRenderPassDescriptor()

renderEncoder = commandBuffer.renderCommandEncoderWithDescriptor_(
  renderPassDescriptor)

#renderEncoder.setRenderPipelineState_(pipelineState)
#renderEncoder.endEncoding()

drawable = view.currentDrawable()
commandBuffer.presentDrawable_(drawable)
#commandBuffer.commit()


# --- MTKViewDelegate
def drawInMTKView_(_self, _cmd, _view):
  self = ObjCInstance(_self)
  view = ObjCInstance(_view)

def mtkView_drawableSizeWillChange_(_self, _cmd, _view, _size):
  self = ObjCInstance(_self)
  view = ObjCInstance(_view)
  _width = _size.width
  _height = _size.height
  aspect = math.fabs(_width / _height)
  projectionMatrix = GLKMatrix4MakePerspective(
    math.radians(65.0), aspect, 4.0, 10.0)
  sceneMatrices.projectionMatrix = projectionMatrix



PyRenderer = create_objc_class(
  name='PyRenderer',
  methods=[drawInMTKView_, mtkView_drawableSizeWillChange_],
  protocols=['MTKViewDelegate'])


class MetalView:
  def __init__(self):
    self.devices = self.createSystemDefaultDevice()
    self.mtkView = ObjCClass('MTKView').alloc()
    self.view_did_load()
    
  def createSystemDefaultDevice(self):
    MTLCreateSystemDefaultDevice = c.MTLCreateSystemDefaultDevice
    MTLCreateSystemDefaultDevice.argtypes = []
    MTLCreateSystemDefaultDevice.restype = ctypes.c_void_p
    return ObjCInstance(MTLCreateSystemDefaultDevice())
    
  

class ViewController(ui.View):
  def __init__(self, *args, **kwargs):
    ui.View.__init__(self, *args, **kwargs)
    self.bg_color = 'slategray'
    self.objc_instance.addSubview_(view)


if __name__ == '__main__':
  view = ViewController()
  view.present(style='fullscreen')

