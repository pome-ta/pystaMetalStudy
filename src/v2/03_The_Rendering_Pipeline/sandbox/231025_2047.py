from pathlib import Path
import ctypes

import numpy as np

from objc_util import ObjCClass, ObjCInstance, create_objc_class, on_main_thread, c, load_framework
from objc_util import sel, CGRect, nsurl

import pdbg

TITLE = '3. The Rendering Pipeline'
shader_path = Path('./final/Shaders.metal')

err_ptr = ctypes.c_void_p()
MTLPrimitiveTypeTriangle = 3

load_framework('SceneKit')

# --- navigation
UINavigationController = ObjCClass('UINavigationController')
UINavigationBarAppearance = ObjCClass('UINavigationBarAppearance')
UIBarButtonItem = ObjCClass('UIBarButtonItem')

# --- viewController
UIViewController = ObjCClass('UIViewController')

# --- view
UIColor = ObjCClass('UIColor')
UILabel = ObjCClass('UILabel')
NSLayoutConstraint = ObjCClass('NSLayoutConstraint')

# --- Metal
MTKView = ObjCClass('MTKView')
MTKMeshBufferAllocator = ObjCClass('MTKMeshBufferAllocator')
MTKMesh = ObjCClass('MTKMesh')
MTLCompileOptions = ObjCClass('MTLCompileOptions')
MTLRenderPipelineDescriptor = ObjCClass('MTLRenderPipelineDescriptor')

# --- Model I/O
MDLMesh = ObjCClass('MDLMesh')

# --- SceneKit
SCNBox = ObjCClass('SCNBox')


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


vector_float3 = np.dtype(
  {
    'names': ['x', 'y', 'z'],
    'formats': [np.float32, np.float32, np.float32],
    'offsets': [_offset * 4 for _offset in range(3)],
    'itemsize': 16,
  },
  align=True)


class Renderer:

  def __init__(self):
    self.device: 'MTLDevice'
    self.commandQueue: 'MTLCommandQueue'
    self.mesh: MTKMesh
    self.vertexBuffer: 'MTLBuffer'
    self.pipelineState: 'MTLRenderPipelineState'

  def _init(self, mtkView: MTKView) -> 'MTKViewDelegate':
    self.device = mtkView.device()
    allocator = MTKMeshBufferAllocator.alloc().initWithDevice_(self.device)

    size = 0.8

    box = SCNBox.boxWithWidth_height_length_chamferRadius_(
      size, size, size, 0.0)

    #pdbg.state(box)
    mdlMesh = MDLMesh.meshWithSCNGeometry_bufferAllocator_(box, allocator)

    self.mesh = MTKMesh.alloc()
    self.mesh.initWithMesh_device_error_(mdlMesh, self.device, err_ptr)

    self.vertexBuffer = self.mesh.vertexBuffers().objectAtIndexedSubscript_(
      0).buffer()

    self.commandQueue = self.device.newCommandQueue()

    source = shader_path.read_text('utf-8')
    library = self.device.newLibraryWithSource_options_error_(
      source, MTLCompileOptions.new(), err_ptr)
    vertexFunction = library.newFunctionWithName_('vertex_main')
    fragmentFunction = library.newFunctionWithName_('fragment_main')

    pipelineDescriptor = MTLRenderPipelineDescriptor.new()
    pipelineDescriptor.colorAttachments().objectAtIndexedSubscript_(
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
      descriptor = view.currentRenderPassDescriptor()

      renderEncoder = commandBuffer.renderCommandEncoderWithDescriptor_(
        descriptor)

      renderEncoder.setRenderPipelineState_(self.pipelineState)
      renderEncoder.setVertexBuffer_offset_atIndex_(self.vertexBuffer, 0, 0)

      for submesh in self.mesh.submeshes():
        indexCount = submesh.indexCount()
        indexType = submesh.indexType()
        indexBuffer = submesh.indexBuffer().buffer()
        indexBufferOffset = submesh.indexBuffer().offset()
        renderEncoder.drawIndexedPrimitives(
          MTLPrimitiveTypeTriangle,
          indexCount=indexCount,
          indexType=indexType,
          indexBuffer=indexBuffer,
          indexBufferOffset=indexBufferOffset)

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
      view.setBackgroundColor_(UIColor.systemDarkExtraLightGrayColor())
      #view.setBackgroundColor_(UIColor.systemBackgroundColor())

      CGRectZero = CGRect((0.0, 0.0), (0.0, 0.0))
      device = MTLCreateSystemDefaultDevice()

      self.mtkView = MTKView.alloc()
      self.mtkView.initWithFrame_device_(CGRectZero, device)
      self.mtkView.clearColor = (1.0, 1.0, 0.8, 1.0)
      self.mtkView.isPaused = True
      self.mtkView.enableSetNeedsDisplay = False

      mtk_layer = self.mtkView.layer()
      mtk_layer.setBorderWidth_(2.0)
      mtk_layer.setBorderColor_(UIColor.systemGrayTintColor().CGColor())

      self.renderer = Renderer.initWithMetalKitView_(self.mtkView)
      self.mtkView.delegate = self.renderer

      label = UILabel.new()
      label.setBackgroundColor_(UIColor.systemDarkLightMidGrayColor())
      label.setTextColor_(UIColor.systemDarkGrayTintColor())
      label.setText_('Hello, Metal! 😇')
      label.sizeToFit()

      label_layer = label.layer()
      label_layer.setBorderWidth_(2.0)
      label_layer.setBorderColor_(UIColor.systemGrayTintColor().CGColor())

      # --- layout
      view.addSubview_(self.mtkView)
      view.addSubview_(label)

      self.mtkView.translatesAutoresizingMaskIntoConstraints = False
      label.translatesAutoresizingMaskIntoConstraints = False

      constraints = [
        # --- mtkView
        self.mtkView.centerXAnchor().constraintEqualToAnchor_(
          view.centerXAnchor()),
        self.mtkView.topAnchor().constraintEqualToAnchor_constant_(
          view.topAnchor(), 20),

        # xxx: 縦横対応してない
        self.mtkView.widthAnchor().constraintEqualToAnchor_multiplier_(
          view.widthAnchor(), 0.9),
        #self.mtkView.heightAnchor().constraintEqualToAnchor_multiplier_(view.widthAnchor(), 1.0),
        self.mtkView.heightAnchor().constraintEqualToAnchor_multiplier_(
          view.widthAnchor(), 0.9),

        # --- label
        label.topAnchor().constraintEqualToAnchor_constant_(
          self.mtkView.bottomAnchor(), 20),
        label.centerXAnchor().constraintEqualToAnchor_(view.centerXAnchor()),
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

  @on_main_thread
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


