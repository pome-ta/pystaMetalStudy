import ctypes
from objc_util import ObjCClass, ObjCInstance, create_objc_class, on_main_thread
from objc_util import c, sel, CGRect

import pdbg

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


def MTLCreateSystemDefaultDevice():
  _MTLCreateSystemDefaultDevice = c.MTLCreateSystemDefaultDevice
  _MTLCreateSystemDefaultDevice.argtypes = []
  _MTLCreateSystemDefaultDevice.restype = ctypes.c_void_p
  return _MTLCreateSystemDefaultDevice()


class AAPLRenderer:

  def __init__(self):
    self._device: 'MTLDevice'
    self._commandQueue: 'MTLCommandQueue'

  def _create_delegate(self):
    # --- `MTKViewDelegate` Methods
    def drawInMTKView_(_self, _cmd, _view):
      this = ObjCInstance(_self)
      view = ObjCInstance(_view)

      renderPassDescriptor = view.currentRenderPassDescriptor()
      commandBuffer = self._commandQueue.commandBuffer()
      commandEncoder = commandBuffer.renderCommandEncoderWithDescriptor_(
        renderPassDescriptor)

      commandEncoder.endEncoding()

      drawable = view.currentDrawable()
      commandBuffer.presentDrawable(drawable)
      commandBuffer.commit()

    def mtkView_drawableSizeWillChange_(_self, _cmd, _view, _size):
      print('mtkView_drawableSizeWillChange_')
      this = ObjCInstance(_self)
      #view = ObjCInstance(_view)
      #size = ObjCInstance(_size)

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

  @on_main_thread
  def _init(self):
    return self._create_delegate()

  @classmethod
  def initWithMetalKitView_(cls, mtkView: MTKView) -> ObjCInstance:
    _cls = cls()
    _cls._device = mtkView.device()
    _cls._commandQueue = _cls._device.newCommandQueue()
    return _cls._init()


class AAPLViewController:

  def __init__(self):
    self._viewController: UIViewController
    self._view: MTKView
    self._renderer: AAPLRenderer

  def _override_viewController(self):
    # --- `UIViewController` Methods
    def viewDidLoad(_self, _cmd):
      this = ObjCInstance(_self)
      view = this.view()

      CGRectZero = CGRect((0.0, 0.0), (0.0, 0.0))
      _device = ObjCInstance(MTLCreateSystemDefaultDevice())

      self._view = MTKView.alloc()
      self._view.initWithFrame_device_(CGRectZero, _device)
      self._view.enableSetNeedsDisplay = True
      self._view.clearColor = (0.0, 0.5, 1.0, 1.0)
      self._renderer = AAPLRenderer.initWithMetalKitView_(self._view)
      self._renderer.mtkView_drawableSizeWillChange_(self._view, view.size())
      self._view.delegate = self._renderer

      view.addSubview_(self._view)
      self._view.translatesAutoresizingMaskIntoConstraints = False

      constraints = [
        self._view.centerXAnchor().constraintEqualToAnchor_(
          view.centerXAnchor()),
        self._view.centerYAnchor().constraintEqualToAnchor_(
          view.centerYAnchor()),
        self._view.widthAnchor().constraintEqualToAnchor_multiplier_(
          view.widthAnchor(), 1.0),
        self._view.heightAnchor().constraintEqualToAnchor_multiplier_(
          view.heightAnchor(), 1.0),
      ]
      NSLayoutConstraint.activateConstraints_(constraints)

    # --- `UIViewController` set up
    _methods = [
      viewDidLoad,
    ]

    create_kwargs = {
      'name': '_aplvc',
      'superclass': UIViewController,
      'methods': _methods,
    }
    _aplvc = create_objc_class(**create_kwargs)
    self._viewController = _aplvc

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
    self._viewController: UIViewController
    self._navigationController: UINavigationController
    self.nav_title = 'nav title'
    

  def _override_navigationController(self):
    # --- `UINavigationController` Methods
    def doneButtonTapped_(_self, _cmd, _sender):
      this = ObjCInstance(_self)

      visibleViewController = this.visibleViewController()
      visibleViewController.dismissViewControllerAnimated_completion_(
        True, None)

    def viewDidLoad(_self, _cmd):
      #print('viewDidLoad')
      this = ObjCInstance(_self)
      view = this.view()

    # --- `UIViewController` set up
    _methods = [
      doneButtonTapped_,
      viewDidLoad,
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
      #appearance.backgroundColor = sc.systemExtraLightGrayColor

      # --- navigationBar
      navigationBar = navigationController.navigationBar()
      '''
      navigationBar.standardAppearance = appearance
      navigationBar.scrollEdgeAppearance = appearance
      navigationBar.compactAppearance = appearance
      navigationBar.compactScrollEdgeAppearance = appearance
      '''

      #navigationBar.prefersLargeTitles = True

      viewController.setEdgesForExtendedLayout_(0)
      #viewController.setExtendedLayoutIncludesOpaqueBars_(True)

      _done_btn = UIBarButtonItem.alloc()
      done_btn = _done_btn.initWithBarButtonSystemItem_target_action_(
        0, navigationController, sel('doneButtonTapped:'))

      visibleViewController = navigationController.visibleViewController()

      # --- navigationItem
      navigationItem = visibleViewController.navigationItem()

      navigationItem.standardAppearance = appearance
      navigationItem.scrollEdgeAppearance = appearance
      navigationItem.compactAppearance = appearance
      navigationItem.compactScrollEdgeAppearance = appearance

      navigationItem.setTitle_('nav')
      navigationItem.rightBarButtonItem = done_btn

    def navigationController_didShowViewController_animated_(
        _self, _cmd, _navigationController, _viewController, _animated):
      #print('did')
      pass

    # --- `UINavigationControllerDelegate` set up
    _methods = [
      navigationController_willShowViewController_animated_,
      navigationController_didShowViewController_animated_,
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
  def _init(self, vc):
    self._override_navigationController()
    nv = self._navigationController.alloc()
    nv.initWithRootViewController_(vc).autorelease()
    _delegate = self.create_navigationControllerDelegate()
    
    nv.nv.setDelegate_(_delegate)
    return nv

  @classmethod
  def new(cls, vc) -> ObjCInstance:
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
  #vc.setModalPresentationStyle(0)
  root_vc.presentViewController_animated_completion_(vc, True, None)


if __name__ == '__main__':
  #ovc = ObjcUIViewController.new()
  #ovc = AAPLViewController.new()
  aplvc = AAPLViewController.new()
  ovc = ObjcUIViewController.new(aplvc)
  present_objc(ovc)

