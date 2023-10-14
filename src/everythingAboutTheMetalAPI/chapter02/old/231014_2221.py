import ctypes

from objc_util import ObjCClass, ObjCInstance, create_objc_class, on_main_thread, load_framework, c
from objc_util import sel, CGRect

import pdbg

TITLE = 'chapter02'

# --- navigation
UINavigationController = ObjCClass('UINavigationController')
UINavigationBarAppearance = ObjCClass('UINavigationBarAppearance')
UIBarButtonItem = ObjCClass('UIBarButtonItem')

# --- viewController
UIViewController = ObjCClass('UIViewController')

# --- view
NSLayoutConstraint = ObjCClass('NSLayoutConstraint')

# --- Metal
load_framework('MetalKit')
MTKView = ObjCClass('MTKView')


def MTLCreateSystemDefaultDevice():
  _MTLCreateSystemDefaultDevice = c.MTLCreateSystemDefaultDevice
  _MTLCreateSystemDefaultDevice.argtypes = []
  _MTLCreateSystemDefaultDevice.restype = ctypes.c_void_p
  return ObjCInstance(_MTLCreateSystemDefaultDevice())


class MetalView:

  def __init__(self):
    self.mtkView: MTKView
    self.devices: 'MTLDevice'
    self.count = 0

  def _override_mtkView(self):

    # --- `MTKView` Methods
    def drawRect_(_self, _cmd, _rect):
      this = ObjCInstance(_self)

      if (drawable :=
          this.currentDrawable()) and (rpd :=
                                       this.currentRenderPassDescriptor()):

        #drawable = this.currentDrawable()
        #rpd = this.currentRenderPassDescriptor()
        rpd.colorAttachments().objectAtIndexedSubscript(
          0).texture = this.currentDrawable().texture()
        rpd.colorAttachments().objectAtIndexedSubscript(0).clearColor = (0.0,
                                                                         0.5,
                                                                         0.5,
                                                                         1.0)
        rpd.colorAttachments().objectAtIndexedSubscript(
          0).loadAction = 2  # .clear

        commandBuffer = this.device().newCommandQueue().commandBuffer()
        commandEncoder = commandBuffer.renderCommandEncoderWithDescriptor_(rpd)
        commandEncoder.endEncoding()
        commandBuffer.presentDrawable_(drawable)
        commandBuffer.commit()
        if self.count < 1:
          print('h')
          #pdbg.state(this)
          #print(rpd.colorAttachments())
          #pdbg.state(rpd.colorAttachments()._descriptorAtIndex_(0))
          #print('--------')
          #pdbg.state(rpd.colorAttachments().objectAtIndexedSubscript(0))
          pdbg.state(this.device())
        self.count += 1

    # --- `MTKView` set up
    _methods = [
      drawRect_,
    ]

    create_kwargs = {
      'name': '_mtk',
      'superclass': MTKView,
      'methods': _methods,
    }
    _mtk = create_objc_class(**create_kwargs)
    self.mtkView = _mtk

  def _init(self):
    self._override_mtkView()
    return self.mtkView

  @classmethod
  def new(cls) -> ObjCInstance:
    _cls = cls()
    return _cls._init()


class ViewController:

  def __init__(self):
    self.device: 'MTLDevice'
    self.mtlView: MTKView

  def _override_viewController(self):

    # --- `UIViewController` Methods
    def viewDidLoad(_self, _cmd):
      this = ObjCInstance(_self)
      view = this.view()

      _mtlView = MetalView.new()

      CGRectZero = CGRect((0.0, 0.0), (0.0, 0.0))

      self.device = MTLCreateSystemDefaultDevice()
      self.mtlView = _mtlView.alloc()
      self.mtlView.initWithFrame_device_(CGRectZero, self.device)

      view.addSubview_(self.mtlView)

      self.mtlView.translatesAutoresizingMaskIntoConstraints = False

      constraints = [
        self.mtlView.centerXAnchor().constraintEqualToAnchor_(
          view.centerXAnchor()),
        self.mtlView.centerYAnchor().constraintEqualToAnchor_(
          view.centerYAnchor()),
        self.mtlView.widthAnchor().constraintEqualToAnchor_multiplier_(
          view.widthAnchor(), 1.0),
        self.mtlView.heightAnchor().constraintEqualToAnchor_multiplier_(
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

      #navigationBar.prefersLargeTitles = True

      viewController.setEdgesForExtendedLayout_(0)
      #viewController.setExtendedLayoutIncludesOpaqueBars_(True)

      done_btn = UIBarButtonItem.alloc(
      ).initWithBarButtonSystemItem_target_action_(0, navigationController,
                                                   sel('doneButtonTapped:'))

      visibleViewController = navigationController.visibleViewController()

      # --- navigationItem
      navigationItem = visibleViewController.navigationItem()
      navigationItem.setTitle_(TITLE)
      navigationItem.rightBarButtonItem = done_btn

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
  ovc = ObjcUIViewController.new(ViewController.new())
  present_objc(ovc)

