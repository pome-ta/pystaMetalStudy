from pathlib import Path
import ctypes

import numpy as np

from objc_util import ObjCClass, ObjCInstance, create_objc_class, on_main_thread, c
from objc_util import sel, CGRect, nsurl

import pdbg

TITLE = '4. The Vertex Function ---start'
#shader_path = Path('./efficient.metal')
#shader_path = Path('./timer.metal')
shader_path = Path('./packed_float3.metal')

err_ptr = ctypes.c_void_p()
MTLPrimitiveTypeTriangle = 3

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
MTLCompileOptions = ObjCClass('MTLCompileOptions')
MTLRenderPipelineDescriptor = ObjCClass('MTLRenderPipelineDescriptor')
MTLVertexDescriptor = ObjCClass('MTLVertexDescriptor')


def MTLCreateSystemDefaultDevice():
  _MTLCreateSystemDefaultDevice = c.MTLCreateSystemDefaultDevice
  _MTLCreateSystemDefaultDevice.argtypes = []
  _MTLCreateSystemDefaultDevice.restype = ctypes.c_void_p
  return ObjCInstance(_MTLCreateSystemDefaultDevice())


Float = np.dtype(np.float32, align=True)
UInt16 = np.dtype(np.uint16, align=True)
Vertex = np.dtype({
  'names': ['x', 'y', 'z',],
  'formats': [Float, Float, Float,],
  'offsets': [o * Float.itemsize for o in range(3)],
  'itemsize': 3 * Float.itemsize,
}, align=True)  # yapf: disable
simd_float3 = np.dtype({
  'names': ['x', 'y', 'z',],
  'formats': [Float, Float, Float,],
  'offsets': [o * Float.itemsize for o in range(3)],
  'itemsize': 16,
}, align=True)  # yapf: disable



class Quad:

  _oldVertices = np.array(
    (
      -1,  1,  0,  # triangle 1
       1, -1,  0,
      -1, -1,  0,
      -1,  1,  0,  # triangle 2
       1,  1,  0,
       1, -1,  0,
    ),
    dtype=Float)  # yapf: disable

  _vertices = np.array(
    (
      -1,  1,  0,
       1,  1,  0,
      -1, -1,  0,
       1, -1,  0,
    ),
    dtype=Float)  # yapf: disable

  _indices = np.array(
    (
      0, 3, 2,
      0, 1, 3,
    ),
    dtype=UInt16)  # yapf: disable

  def __init__(self, device: 'MTLDevice', scale: float = 1.0):
    self.vertexBuffer: 'MTLBuffer'
    self.indexBuffer: 'MTLBuffer'

    self.vertices = Quad._vertices * scale
    v_bytes = self.vertices.ctypes
    v_length = Float.itemsize * self.vertices.size

    self.vertexBuffer = device.newBufferWithBytes(v_bytes,
                                                  length=v_length,
                                                  options=0)

    self.indices = Quad._indices
    i_bytes = self.indices.ctypes
    i_length = UInt16.itemsize * self.indices.size
    self.indexBuffer = device.newBufferWithBytes(i_bytes,
                                                 length=i_length,
                                                 options=0)
    print(self.indices)
    print(self.indexBuffer)
    print(UInt16.itemsize)
    print(self.indices.size)


class Renderer:

  def __init__(self):
    self.device: 'MTLDevice'
    self.commandQueue: 'MTLCommandQueue'
    self.library: 'MTLLibrary'
    self.pipelineState: 'MTLRenderPipelineState'

    self.quad: Quad
    self.timer: Float = np.array(0.0, dtype=Float)

  def _init(self, mtkView: MTKView) -> 'MTKViewDelegate':
    self.device = mtkView.device()
    self.commandQueue = self.device.newCommandQueue()
    self.quad = Quad(self.device, 0.8)

    source = shader_path.read_text('utf-8')
    self.library = self.device.newLibraryWithSource(
      source, options=MTLCompileOptions.new(), error=err_ptr)

    vertexFunction = self.library.newFunctionWithName('vertex_main')
    fragmentFunction = self.library.newFunctionWithName('fragment_main')

    pipelineDescriptor = MTLRenderPipelineDescriptor.new()
    pipelineDescriptor.vertexFunction = vertexFunction
    pipelineDescriptor.fragmentFunction = fragmentFunction
    pipelineDescriptor.colorAttachments().objectAtIndexedSubscript(
      0).pixelFormat = mtkView.colorPixelFormat()

    pipelineDescriptor.vertexDescriptor = MTLVertexDescriptor.vertexDescriptor(
    )

    self.pipelineState = self.device.newRenderPipelineStateWithDescriptor(
      pipelineDescriptor, error=err_ptr)

    return self._create_delegate()

  def _create_delegate(self):
    # --- `MTKViewDelegate` Methods
    def drawInMTKView_(_self, _cmd, _view):
      view = ObjCInstance(_view)

      commandBuffer = self.commandQueue.commandBuffer()
      descriptor = view.currentRenderPassDescriptor()

      renderEncoder = commandBuffer.renderCommandEncoderWithDescriptor(
        descriptor)

      self.timer += 0.005
      currentTime = np.array(np.sin(self.timer), dtype=Float)

      renderEncoder.setVertexBytes(currentTime.ctypes,
                                   length=Float.itemsize,
                                   atIndex=11)

      renderEncoder.setRenderPipelineState(self.pipelineState)
      renderEncoder.setVertexBuffer(self.quad.vertexBuffer,
                                    offset=0,
                                    atIndex=0)

      #renderEncoder.setVertexBuffer(self.quad.indexBuffer, offset=0, atIndex=1)

      renderEncoder.drawPrimitives(MTLPrimitiveTypeTriangle,
                                   vertexStart=0,
                                   vertexCount=self.quad.indices.size)
      #renderEncoder.drawPrimitives(MTLPrimitiveTypeTriangle, vertexStart=0, vertexCount=self.quad.vertices.size)
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
      view.setBackgroundColor(UIColor.systemDarkExtraLightGrayColor())
      #view.setBackgroundColor_(UIColor.systemBackgroundColor())

      CGRectZero = CGRect((0.0, 0.0), (0.0, 0.0))
      device = MTLCreateSystemDefaultDevice()

      self.mtkView = MTKView.alloc()
      self.mtkView.initWithFrame(CGRectZero, device=device)
      self.mtkView.clearColor = (1.0, 1.0, 0.8, 1.0)
      self.mtkView.isPaused = True
      self.mtkView.enableSetNeedsDisplay = False

      mtk_layer = self.mtkView.layer()
      mtk_layer.setBorderWidth(2.0)
      mtk_layer.setBorderColor(UIColor.systemGrayTintColor().CGColor())

      self.renderer = Renderer.initWithMetalKitView_(self.mtkView)
      self.mtkView.delegate = self.renderer

      label = UILabel.new()
      label.setBackgroundColor(UIColor.systemDarkLightMidGrayColor())
      label.setTextColor(UIColor.systemDarkGrayTintColor())
      label.setText('Hello, Metal! 😇')
      label.sizeToFit()

      label_layer = label.layer()
      label_layer.setBorderWidth(2.0)
      label_layer.setBorderColor(UIColor.systemGrayTintColor().CGColor())

      # --- layout
      view.addSubview(self.mtkView)
      view.addSubview(label)

      self.mtkView.translatesAutoresizingMaskIntoConstraints = False
      label.translatesAutoresizingMaskIntoConstraints = False

      constraints = [
        # --- mtkView
        self.mtkView.centerXAnchor().constraintEqualToAnchor(
          view.centerXAnchor()),
        self.mtkView.topAnchor().constraintEqualToAnchor(view.topAnchor(),
                                                         constant=8),

        # xxx: 縦横対応してない
        self.mtkView.widthAnchor().constraintEqualToAnchor(view.widthAnchor(),
                                                           multiplier=0.96),
        #self.mtkView.heightAnchor().constraintEqualToAnchor_multiplier_(view.widthAnchor(), 1.0),
        self.mtkView.heightAnchor().constraintEqualToAnchor(
          view.heightAnchor(), multiplier=0.64),

        # --- label
        label.topAnchor().constraintEqualToAnchor(self.mtkView.bottomAnchor(),
                                                  constant=8),
        label.centerXAnchor().constraintEqualToAnchor(view.centerXAnchor()),
      ]
      NSLayoutConstraint.activateConstraints(constraints)

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
      visibleViewController.dismissViewControllerAnimated(True,
                                                          completion=None)

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

      viewController.setEdgesForExtendedLayout(0)
      #viewController.setExtendedLayoutIncludesOpaqueBars_(True)

      done_btn = UIBarButtonItem.alloc().initWithBarButtonSystemItem(
        0, target=navigationController, action=sel('doneButtonTapped:'))

      visibleViewController = navigationController.visibleViewController()

      # --- navigationItem
      navigationItem = visibleViewController.navigationItem()
      navigationItem.rightBarButtonItem = done_btn
      navigationItem.setTitle(TITLE)

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
    nv.initWithRootViewController(vc).autorelease()
    nv.setDelegate(_delegate)
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
  root_vc.presentViewController(vc, animated=True, completion=None)


if __name__ == '__main__':
  mtlvc = MetalViewController.new()
  ovc = ObjcUIViewController.new(mtlvc)
  present_objc(ovc)


