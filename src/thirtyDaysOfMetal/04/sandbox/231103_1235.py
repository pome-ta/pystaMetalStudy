import ctypes

from objc_util import ObjCClass, ObjCInstance, create_objc_class, on_main_thread, c
from objc_util import sel, CGRect, nsurl

import pdbg

TITLE = 'Day 4'

err_ptr = ctypes.c_void_p()
MTLPrimitiveTypeTriangle = 3

# --- UIKit
UIViewController = ObjCClass('UIViewController')
UIColor = ObjCClass('UIColor')

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
    #pipelineDescriptor.colorAttachments().objectAtIndexedSubscript(0).pixelFormat = mtkView.colorPixelFormat()

    pipelineDescriptor.vertexDescriptor = MTLVertexDescriptor.vertexDescriptor(
    )
    #pipelineDescriptor.vertexDescriptor = MTLVertexDescriptor.new()

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

      #self.timer += 0.005
      currentTime = np.array(np.sin(self.timer), dtype=Float)

      renderEncoder.setVertexBytes(currentTime.ctypes,
                                   length=Float.itemsize,
                                   atIndex=11)

      renderEncoder.setRenderPipelineState(self.pipelineState)
      renderEncoder.setVertexBuffer(self.quad.vertexBuffer,
                                    offset=0,
                                    atIndex=0)

      renderEncoder.setVertexBuffer(self.quad.indexBuffer, offset=0, atIndex=1)

      renderEncoder.drawPrimitives(MTLPrimitiveTypeTriangle,
                                   vertexStart=0,
                                   vertexCount=self.quad.indices.size)
      #renderEncoder.drawPrimitives(MTLPrimitiveTypeTriangle, vertexStart=0, vertexCount=self.quad.vertices.size)

      #renderEncoder.drawIndexedPrimitives_indexCount_indexType_indexBuffer_indexBufferOffset_(3, self.indices.__len__(), 0, self.indexBuffer, 0)  # .triangle

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

      CGRectZero = CGRect((0.0, 0.0), (0.0, 0.0))
      device = MTLCreateSystemDefaultDevice()

      self.mtkView = MTKView.alloc()
      self.mtkView.initWithFrame(CGRectZero, device=device)
      self.mtkView.clearColor = (1.0, 1.0, 0.8, 1.0)
      #self.mtkView.isPaused = True
      #self.mtkView.enableSetNeedsDisplay = False

      self.renderer = Renderer.initWithMetalKitView_(self.mtkView)
      self.mtkView.delegate = self.renderer

      # --- layout
      view.addSubview(self.mtkView)
      self.mtkView.translatesAutoresizingMaskIntoConstraints = False

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
      ]

      ObjCClass('NSLayoutConstraint').activateConstraints(constraints)

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
      'superclass': ObjCClass('UINavigationController'),
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
      appearance = ObjCClass('UINavigationBarAppearance').alloc()
      appearance.configureWithDefaultBackground()

      # --- navigationBar
      navigationBar = navigationController.navigationBar()

      navigationBar.standardAppearance = appearance
      navigationBar.scrollEdgeAppearance = appearance
      navigationBar.compactAppearance = appearance
      navigationBar.compactScrollEdgeAppearance = appearance

      navigationBar.prefersLargeTitles = True

      viewController.setEdgesForExtendedLayout(0)
      #viewController.setExtendedLayoutIncludesOpaqueBars_(True)

      uiBarButtonItem = ObjCClass('UIBarButtonItem').alloc()
      done_btn = uiBarButtonItem.initWithBarButtonSystemItem(
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
  vc.setModalPresentationStyle(0)
  root_vc.presentViewController(vc, animated=True, completion=None)


if __name__ == '__main__':
  mtlvc = MetalViewController.new()
  ovc = ObjcUIViewController.new(mtlvc)
  present_objc(ovc)

