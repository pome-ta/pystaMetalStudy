from pathlib import Path
import math
import ctypes

from objc_util import c, create_objc_class, ObjCClass, ObjCInstance
import ui

import pdbg

# --- load Shader code
shader_path = Path('./Shaders01.py')

# --- load objc classes
MTKView = ObjCClass('MTKView')
MTLRenderPipelineDescriptor = ObjCClass('MTLRenderPipelineDescriptor')

# todo: MetalDevice
MTLCreateSystemDefaultDevice = c.MTLCreateSystemDefaultDevice
MTLCreateSystemDefaultDevice.argtypes = []
MTLCreateSystemDefaultDevice.restype = ctypes.c_void_p

err_ptr = ctypes.c_void_p()

# --- GLKit MathMatrix
# https://github.com/Cethric/OpenGLES-Pythonista/blob/master/GLKit/glkmath/matrix4.py
class float16(ctypes.Structure):
  _fields_ = [('m', (ctypes.c_float * 16)),]

class m16(ctypes.Structure):
  _fields_ = [('m00', ctypes.c_float),
              ('m01', ctypes.c_float),
              ('m02', ctypes.c_float),
              ('m03', ctypes.c_float),
              ('m10', ctypes.c_float),
              ('m11', ctypes.c_float),
              ('m12', ctypes.c_float),
              ('m13', ctypes.c_float),
              ('m20', ctypes.c_float),
              ('m21', ctypes.c_float),
              ('m22', ctypes.c_float),
              ('m23', ctypes.c_float),
              ('m30', ctypes.c_float),
              ('m31', ctypes.c_float),
              ('m32', ctypes.c_float),
              ('m33', ctypes.c_float),]

class GLKMatrix4(ctypes.Union):
  _anonymous_ = [('s1'), ('s2'),]
  _fields_ = [('s1', float16), ('s2', m16),]
  
  def __str__(self):
    mstr = '''GLKMatrix4 {\n{%.3f, %.3f, %.3f, %.3f}\n{%.3f, %.3f, %.3f, %.3f}\n{%.3f, %.3f, %.3f, %.3f}\n{%.3f, %.3f, %.3f, %.3f}\n}''' % tuple([float(x) for x in self.s1.m])
    return mstr

def GLKMatrix4Make(m00, m01, m02, m03, m10, m11, m12, m13, m20, m21, m22, m23, m30, m31, m32, m33):
  matrix = GLKMatrix4()
  matrix.m00 = m00
  matrix.m01 = m01
  matrix.m02 = m02
  matrix.m03 = m03
  matrix.m10 = m10
  matrix.m11 = m11
  matrix.m12 = m12
  matrix.m13 = m13
  matrix.m20 = m20
  matrix.m21 = m21
  matrix.m22 = m22
  matrix.m23 = m23
  matrix.m30 = m30
  matrix.m31 = m31
  matrix.m32 = m32
  matrix.m33 = m33
  return matrix

def GLKMatrix4MakeWithArray(values):
  return GLKMatrix4Make(*values)


def GLKMatrix4Identity():
  return GLKMatrix4Make(1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1)

def GLKMatrix4MakeTranslation(tx, ty, tz):
  m = GLKMatrix4Identity()
  m.m[12] = tx
  m.m[13] = ty
  m.m[14] = tz
  return m

def GLKMatrix4MakePerspective(fovyRadians, aspect, nearZ, farZ):
  cotan = 1.0 / math.tan(fovyRadians / 2.0);
  array = [cotan / aspect, 0.0, 0.0, 0.0,
           0.0, cotan, 0.0, 0.0,
           0.0, 0.0, (farZ + nearZ) / (nearZ - farZ), -1.0,
           0.0, 0.0, (2.0 * farZ * nearZ) / (nearZ - farZ), 0.0]
  return GLKMatrix4MakeWithArray(array)
    



# --- Structure
vertices = ((ctypes.c_float * 7) * 4)(
  ( 1.0, -1.0, 0.0, 1.0, 0.0, 0.0, 1.0),
  ( 1.0,  1.0, 0.0, 0.0, 1.0, 0.0, 1.0),
  (-1.0,  1.0, 0.0, 0.0, 0.0, 1.0, 1.0),
  (-1.0, -1.0, 0.0, 0.0, 0.0, 0.0, 1.0))


indices = (ctypes.c_uint32 * 6)(0, 1, 2, 2, 3, 0)

class SceneMatrices(ctypes.Structure):
  # todo: add `def __str__(self):` ?
  _fields_ = [
    ('projectionMatrix', GLKMatrix4),
    ('modelviewMatrix', GLKMatrix4)]
    
  def __init__(self):
    super(ctypes.Structure, self).__init__()
    self.projectionMatrix = GLKMatrix4Identity()
    self.modelviewMatrix = GLKMatrix4Identity()

sceneMatrices = SceneMatrices()


class MetalView(ui.View):
  def __init__(self, *args, **kwargs):
    ui.View.__init__(self, *args, **kwargs)
    self.bg_color = 'maroon'
    self.view_did_load()

  def view_did_load(self):
    mtkView = MTKView.alloc()
    _device = MTLCreateSystemDefaultDevice()
    devices = ObjCInstance(_device)
    '''
    # todo: 端末サイズにて要調整
    _uw, _uh = ui.get_window_size()
    _w = min(_uw, _uh) * 0.96
    _x = (_uw - _w) / 2
    _y = _uh / 4
    _frame = ((_x, _y), (_w, _w))
    '''
    _frame = ((0.0, 0.0), (128.0, 128.0))

    mtkView.initWithFrame_device_(_frame, devices)
    mtkView.setAutoresizingMask_((1 << 1) | (1 << 4))

    renderer = self.renderer_init(PyRenderer, mtkView)
    mtkView.delegate = renderer
    #mtkView.enableSetNeedsDisplay = True
    #mtkView.framebufferOnly = False
    #mtkView.setNeedsDisplay()
    self.objc_instance.addSubview_(mtkView)

  def renderer_init(self, delegate, _mtkView):
    renderer = delegate.alloc().init()
    device = _mtkView.device()
    renderer.commandQueue = device.newCommandQueue()

    renderer.vertexBuffer = device.newBufferWithBytes_length_options_(
      vertices, ctypes.sizeof(vertices), 0)
    renderer.indicesBuffer = device.newBufferWithBytes_length_options_(
      indices, ctypes.sizeof(indices), 0)

    source = shader_path.read_text('utf-8')
    library = device.newLibraryWithSource_options_error_(
      source, err_ptr, err_ptr)

    vertex_func = library.newFunctionWithName_('basic_vertex')
    frag_func = library.newFunctionWithName_('basic_fragment')

    rpld = MTLRenderPipelineDescriptor.new()
    rpld.vertexFunction = vertex_func
    rpld.fragmentFunction = frag_func
    rpld.colorAttachments().objectAtIndexedSubscript(
      0).pixelFormat = 80  # .bgra8Unorm

    renderer.rps = device.newRenderPipelineStateWithDescriptor_error_(
      rpld, err_ptr)
      
    renderer.rotation = 0.0
    renderer.preferredFramesTime = 1.0 / _mtkView.preferredFramesPerSecond()


    return renderer


# --- MTKViewDelegate
def drawInMTKView_(_self, _cmd, _view):
  self = ObjCInstance(_self)
  view = ObjCInstance(_view)

  drawable = view.currentDrawable()
  rpd = view.currentRenderPassDescriptor()
  rpd.colorAttachments().objectAtIndexedSubscript(
    0).texture = drawable.texture()
  rpd.colorAttachments().objectAtIndexedSubscript(
    0).loadAction = 2  # .clear
  rpd.colorAttachments().objectAtIndexedSubscript(
    0).clearColor = (0.85, 0.85, 0.85, 1.0)

  commandBuffer = self.commandQueue.commandBuffer()
  commandEncoder = commandBuffer.renderCommandEncoderWithDescriptor_(rpd)

  commandEncoder.setRenderPipelineState_(self.rps)

  commandEncoder.setVertexBuffer_offset_atIndex_(self.vertexBuffer, 0, 0)
  commandEncoder.drawIndexedPrimitives_indexCount_indexType_indexBuffer_indexBufferOffset_(
    3, 6, 1, self.indicesBuffer, 0)

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
