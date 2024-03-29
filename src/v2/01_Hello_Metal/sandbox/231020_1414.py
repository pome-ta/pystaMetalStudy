#import pathlib
import ctypes

import numpy as np

from objc_util import ObjCClass, ObjCInstance
from objc_util import create_objc_class, on_main_thread, c, load_framework
from objc_util import sel, CGRect

import pdbg

TITLE = '1. Hello, Metal!'
err_ptr = ctypes.c_void_p()

#load_framework('ModelIO')

# --- navigation
UINavigationController = ObjCClass('UINavigationController')
UINavigationBarAppearance = ObjCClass('UINavigationBarAppearance')
UIBarButtonItem = ObjCClass('UIBarButtonItem')

# --- viewController
UIViewController = ObjCClass('UIViewController')

# --- view
NSLayoutConstraint = ObjCClass('NSLayoutConstraint')

# --- Metal
MTKView = ObjCClass('MTKView')
MTLCompileOptions = ObjCClass('MTLCompileOptions')
MTLRenderPipelineDescriptor = ObjCClass('MTLRenderPipelineDescriptor')
MTKMeshBufferAllocator = ObjCClass('MTKMeshBufferAllocator')

MDLMesh = ObjCClass('MDLMesh')
MTKMesh = ObjCClass('MTKMesh')

vector_float3 = np.dtype(
  {
    'names': ['x', 'y', 'z'],
    'formats': [np.float32, np.float32, np.float32],
    'offsets': [_offset * 4 for _offset in range(3)],
    'itemsize': 16,
  },
  align=True)

vector_uint2 = np.dtype(
  {
    'names': ['x', 'y'],
    'formats': [np.uint32, np.uint32],
    'offsets': [_offset * 4 for _offset in range(2)],
    'itemsize': 8,
  },
  align=True)


def MTLCreateSystemDefaultDevice():
  _MTLCreateSystemDefaultDevice = c.MTLCreateSystemDefaultDevice
  _MTLCreateSystemDefaultDevice.argtypes = []
  _MTLCreateSystemDefaultDevice.restype = ctypes.c_void_p
  return ObjCInstance(_MTLCreateSystemDefaultDevice())


def MTKMetalVertexDescriptorFromModelIO(modelIODescriptor):
  _MTKMetalVertexDescriptorFromModelIO = c.MTKMetalVertexDescriptorFromModelIO
  _MTKMetalVertexDescriptorFromModelIO.argtypes = [ctypes.c_void_p]
  _MTKMetalVertexDescriptorFromModelIO.restype = ctypes.c_void_p
  _ptr = _MTKMetalVertexDescriptorFromModelIO(modelIODescriptor)
  return ObjCInstance(_ptr)


shader = '''
#include <metal_stdlib>
using namespace metal;

struct VertexIn {
  float4 position [[attribute(0)]];
};

vertex float4 vertex_main(const VertexIn vertex_in [[stage_in]]) {
  return vertex_in.position;
}

fragment float4 fragment_main() {
  return float4(1, 0, 0, 1);
}
'''


class Renderer:

  def __init__(self):
    self.device: 'MTLDevice'
    self.commandQueue: 'MTLCommandQueue'
    self.allocator: MTKMeshBufferAllocator
    self.mesh: None
    self.pipelineState = None

  def _init(self, mtkView: MTKView) -> 'MTKViewDelegate':
    self.device = mtkView.device()
    self.allocator = MTKMeshBufferAllocator.alloc().initWithDevice_(
      self.device)

    # xxx: 球体諦め
    mdlMesh = MDLMesh.newIcosahedronWithRadius_inwardNormals_allocator_(
      100.0, False, self.allocator)

    self.mesh = MTKMesh.alloc().initWithMesh_device_error_(
      mdlMesh, self.device, err_ptr)

    self.commandQueue = self.device.newCommandQueue()
    library = self.device.newLibraryWithSource_options_error_(
      shader, None, err_ptr)
    vertexFunction = library.newFunctionWithName_('vertex_main')
    fragmentFunction = library.newFunctionWithName_('fragment_main')

    pipelineDescriptor = MTLRenderPipelineDescriptor.new()
    pipelineDescriptor.colorAttachments().objectAtIndexedSubscript(
      0).pixelFormat = 80  # .bgra8Unorm
    pipelineDescriptor.vertexFunction = vertexFunction
    pipelineDescriptor.fragmentFunction = fragmentFunction
    pipelineDescriptor.vertexDescriptor = MTKMetalVertexDescriptorFromModelIO(
      self.mesh.vertexDescriptor())

    self.pipelineState = self.device.newRenderPipelineStateWithDescriptor_error_(
      pipelineDescriptor, err_ptr)

    return self._create_delegate()

  def _create_delegate(self):
    # --- `MTKViewDelegate` Methods
    def drawInMTKView_(_self, _cmd, _view):
      this = ObjCInstance(_self)
      view = ObjCInstance(_view)

      commandBuffer = self.commandQueue.commandBuffer()
      renderPassDescriptor = view.currentRenderPassDescriptor()

      renderEncoder = commandBuffer.renderCommandEncoderWithDescriptor_(
        renderPassDescriptor)
      renderEncoder.setRenderPipelineState_(self.pipelineState)

      _buffer = self.mesh.vertexBuffers().objectAtIndexedSubscript(0).buffer()
      renderEncoder.setVertexBuffer_offset_atIndex_(_buffer, 0, 0)

      submesh = self.mesh.submeshes().firstObject()
      renderEncoder.drawIndexedPrimitives_indexCount_indexType_indexBuffer_indexBufferOffset_(
        3, submesh.indexCount(), submesh.indexType(),
        submesh.indexBuffer().buffer(), 0)

      renderEncoder.endEncoding()
      drawable = view.currentDrawable()
      commandBuffer.presentDrawable_(drawable)
      commandBuffer.commit()

    def mtkView_drawableSizeWillChange_(_self, _cmd, _view, _size):
      pass

    # --- `MTKViewDelegate` set up
    _methods = [
      drawInMTKView_,
      mtkView_drawableSizeWillChange_,
    ]
    _protocols = [
      'MTKViewDelegate',
    ]

    create_kwargs = {
      'name': '_delegate',
      'methods': _methods,
      'protocols': _protocols,
    }

    _delegate = create_objc_class(**create_kwargs)
    return _delegate.new()

  @classmethod
  def initWithMetalKitView_(cls, mtkView: MTKView) -> 'MTKViewDelegate':
    _cls = cls()
    return _cls._init(mtkView)


class MetalViewController:

  def __init__(self):
    self._viewController: UIViewController
    self.mtkView: MTKView
    self.renderer: Renderer

  def _override_viewController(self):

    # --- `UIViewController` Methods
    def viewDidLoad(_self, _cmd):
      this = ObjCInstance(_self)
      view = this.view()

      CGRectZero = CGRect((0.0, 0.0), (0.0, 0.0))
      device = MTLCreateSystemDefaultDevice()

      self.mtkView = MTKView.alloc()
      self.mtkView.initWithFrame_device_(CGRectZero, device)
      self.mtkView.clearColor = (1.0, 1.0, 0.8, 1.0)

      self.renderer = Renderer.initWithMetalKitView_(self.mtkView)
      self.mtkView.delegate = self.renderer

      # --- layout
      view.addSubview_(self.mtkView)
      self.mtkView.translatesAutoresizingMaskIntoConstraints = False

      constraints = [
        self.mtkView.centerXAnchor().constraintEqualToAnchor_(
          view.centerXAnchor()),
        self.mtkView.centerYAnchor().constraintEqualToAnchor_(
          view.centerYAnchor()),
        self.mtkView.widthAnchor().constraintEqualToAnchor_multiplier_(
          view.widthAnchor(), 1.0),
        self.mtkView.heightAnchor().constraintEqualToAnchor_multiplier_(
          view.heightAnchor(), 1.0),
      ]
      NSLayoutConstraint.activateConstraints_(constraints)

    # --- `UIViewController` set up
    _methods = [
      viewDidLoad,
    ]

    create_kwargs = {
      'name': '_vc',
      'superclass': UIViewController,
      'methods': _methods,
    }
    _vc = create_objc_class(**create_kwargs)
    self._viewController = _vc

  #@on_main_thread
  def _init(self):
    self._override_viewController()
    vc = self._viewController.new().autorelease()
    return vc

  @classmethod
  def new(cls) -> ObjCInstance:
    _cls = cls()
    return _cls._init()


class ObjcUIViewController:

  def __init__(self):
    self._navigationController: UINavigationController

  def _override_navigationController(self):
    # --- `UINavigationController` Methods
    def doneButtonTapped_(_self, _cmd, _sender):
      this = ObjCInstance(_self)
      visibleViewController = this.visibleViewController()
      visibleViewController.dismissViewControllerAnimated_completion_(
        True, None)

    # --- `UINavigationController` set up
    _methods = [
      doneButtonTapped_,
    ]

    create_kwargs = {
      'name': '_nv',
      'superclass': UINavigationController,
      'methods': _methods,
    }
    _nv = create_objc_class(**create_kwargs)
    self._navigationController = _nv

  def create_navigationControllerDelegate(self):
    # --- `UINavigationControllerDelegate` Methods
    def navigationController_willShowViewController_animated_(
        _self, _cmd, _navigationController, _viewController, _animated):

      navigationController = ObjCInstance(_navigationController)
      viewController = ObjCInstance(_viewController)

      # --- appearance
      appearance = UINavigationBarAppearance.alloc()
      appearance.configureWithDefaultBackground()
      #appearance.configureWithOpaqueBackground()
      #appearance.configureWithTransparentBackground()

      # --- navigationBar
      navigationBar = navigationController.navigationBar()

      navigationBar.standardAppearance = appearance
      navigationBar.scrollEdgeAppearance = appearance
      navigationBar.compactAppearance = appearance
      navigationBar.compactScrollEdgeAppearance = appearance

      navigationBar.prefersLargeTitles = True

      viewController.setEdgesForExtendedLayout_(0)
      #viewController.setExtendedLayoutIncludesOpaqueBars_(True)

      done_btn = UIBarButtonItem.alloc(
      ).initWithBarButtonSystemItem_target_action_(0, navigationController,
                                                   sel('doneButtonTapped:'))

      visibleViewController = navigationController.visibleViewController()

      # --- navigationItem
      navigationItem = visibleViewController.navigationItem()
      navigationItem.rightBarButtonItem = done_btn
      navigationItem.setTitle_(TITLE)

    # --- `UINavigationControllerDelegate` set up
    _methods = [
      navigationController_willShowViewController_animated_,
    ]
    _protocols = [
      'UINavigationControllerDelegate',
    ]

    create_kwargs = {
      'name': '_nvDelegate',
      'methods': _methods,
      'protocols': _protocols,
    }
    _nvDelegate = create_objc_class(**create_kwargs)
    return _nvDelegate.new()

  @on_main_thread
  def _init(self, vc: UIViewController):
    self._override_navigationController()
    _delegate = self.create_navigationControllerDelegate()
    nv = self._navigationController.alloc()
    nv.initWithRootViewController_(vc).autorelease()
    nv.setDelegate_(_delegate)
    return nv

  @classmethod
  def new(cls, vc: UIViewController) -> ObjCInstance:
    _cls = cls()
    return _cls._init(vc)


@on_main_thread
def present_objc(vc):
  app = ObjCClass('UIApplication').sharedApplication()
  window = app.keyWindow() if app.keyWindow() else app.windows().firstObject()

  root_vc = window.rootViewController()

  while root_vc.presentedViewController():
    root_vc = root_vc.presentedViewController()
  '''
  case -2 : automatic
  case -1 : none
  case  0 : fullScreen
  case  1 : pageSheet <- default ?
  case  2 : formSheet
  case  3 : currentContext
  case  4 : custom
  case  5 : overFullScreen
  case  6 : overCurrentContext
  case  7 : popover
  case  8 : blurOverFullScreen
  '''
  vc.setModalPresentationStyle(0)
  root_vc.presentViewController_animated_completion_(vc, True, None)


if __name__ == '__main__':
  mtlvc = MetalViewController.new()
  ovc = ObjcUIViewController.new(mtlvc)
  present_objc(ovc)

