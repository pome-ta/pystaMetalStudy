import pathlib
from math import sin, cos
import ctypes
from objc_util import c, create_objc_class, ObjCClass, ObjCInstance
import ui

import pdbg

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


# xxx: クソダサ
def create_vertex(structure, array):
  for s1, a1 in enumerate(array):
    for s2, a2 in enumerate(a1):
      for s3, a3 in enumerate(a2):
        structure[s1][s2][s3] = a3
  return structure


# --- set Vertex
Vertex = (((ctypes.c_float * 4) * 2) * 8)()

bf_array = [
  [[-1.0, -1.0,  1.0, 1.0], [1.0, 1.0, 1.0, 1.0]],
  [[ 1.0, -1.0,  1.0, 1.0], [1.0, 0.0, 0.0, 1.0]],
  [[ 1.0,  1.0,  1.0, 1.0], [1.0, 1.0, 0.0, 1.0]],
  [[-1.0,  1.0,  1.0, 1.0], [0.0, 1.0, 0.0, 1.0]],
  [[-1.0, -1.0, -1.0, 1.0], [0.0, 0.0, 1.0, 1.0]],
  [[ 1.0, -1.0, -1.0, 1.0], [1.0, 0.0, 1.0, 1.0]],
  [[-1.0,  1.0, -1.0, 1.0], [0.0, 0.0, 0.0, 1.0]],
  [[-1.0,  1.0, -1.0, 1.0], [0.0, 1.0, 1.0, 1.0]]
  ]

vertexData = create_vertex(Vertex, bf_array)



indexData = (ctypes.c_int16 * 36)()
bf_index = [0, 1, 2, 2, 3, 0,   # front
            1, 5, 6, 6, 2, 1,   # right
            3, 2, 6, 6, 7, 3,   # top
            4, 5, 1, 1, 0, 4,   # bottom
            4, 0, 3, 3, 7, 4,   # left
            7, 6, 5, 5, 4, 7]   # back


for ni, ii in enumerate(bf_index):
  indexData[ni] = ii



class Matrix:
  def __init__(self):
    bf_m = [
      1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0,
      0.0, 1.0
    ]
    m = (ctypes.c_float * 16)()
    for n, i in enumerate(bf_m):
      m[n] = i
    self.m = m

  def translationMatrix(self, matrix, position):
    matrix.m[12] = position[0]
    matrix.m[13] = position[1]
    matrix.m[14] = position[2]
    return matrix

  def scalingMatrix(self, matrix, scale):
    matrix.m[0] = scale
    matrix.m[5] = scale
    matrix.m[10] = scale
    matrix.m[15] = 1.0
    return matrix

  def rotationMatrix(self, matrix, rot):
    matrix.m[0] = cos(rot[1]) * cos(rot[2])
    matrix.m[
      4] = cos(rot[2]) * sin(rot[0]) * sin(rot[1]) - cos(rot[0]) * sin(rot[2])
    matrix.m[
      8] = cos(rot[0]) * cos(rot[2]) * sin(rot[1]) + sin(rot[0]) * sin(rot[2])
    matrix.m[1] = cos(rot[1]) * sin(rot[2])
    matrix.m[
      5] = cos(rot[0]) * cos(rot[2]) + sin(rot[0]) * sin(rot[1]) * sin(rot[2])
    matrix.m[9] = -cos(rot[2]) * sin(rot[0]) + cos(rot[0]) * sin(rot[1]) * sin(
      rot[2])
    matrix.m[2] = -sin(rot[1])
    matrix.m[6] = cos(rot[1]) * sin(rot[0])
    matrix.m[10] = cos(rot[0]) * cos(rot[1])
    matrix.m[15] = 1.0
    return matrix

  def modelMatrix(self, matrix):
    #matrix = self.rotationMatrix(matrix, [0.0, 0.0, 0.1])
    #matrix = self.scalingMatrix(matrix, 0.25)
    #matrix = self.translationMatrix(matrix, [0.0, 0.5, 0.0])

    return matrix


m_byt = Matrix().modelMatrix(Matrix()).m


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

    # --- createBuffer
    renderer.device = _mtkView.device()
    renderer.commandQueue = renderer.device.newCommandQueue()

    # xxx: 要確認
    #dataSize = 16 * (3 * 2)

    renderer.vertexBuffer = renderer.device.newBufferWithBytes_length_options_(vertexData, 16 * (3 * 2), 0)
    
    renderer.indexBuffer = renderer.device.newBufferWithBytes_length_options_(indexData, 16 * 32, 0)
    
    #pdbg.state(renderer.indexBuffer.length())
    
    

    #renderer.uniformBuffer = renderer.device.newBufferWithBytes_length_options_(m_byt, 16 * 16, 0)

    renderer.uniformBuffer = renderer.device.newBufferWithLength_options_(16*16, 0)

    #bufferPointer = renderer.uniformBuffer.contents()


    # --- registerShaders
    source = shader_path.read_text('utf-8')
    library = renderer.device.newLibraryWithSource_options_error_(
      source, MTLCompileOptions.new(), err_ptr)

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
  commandEncoder.setVertexBuffer_offset_atIndex_(self.uniformBuffer, 0, 1)
  #commandEncoder.drawPrimitives_vertexStart_vertexCount_instanceCount_(3, 0, 3, 1)  # .triangle
  commandEncoder.drawIndexedPrimitives_indexCount_indexType_indexBuffer_indexBufferOffset_(3, indexBuffer.length()/16, 0, self.indexBuffer, 0)  # MTLIndexType.uint16  = 0

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

