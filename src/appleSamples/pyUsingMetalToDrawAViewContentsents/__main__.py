import ctypes
from objc_util import ObjCClass, ObjCInstance, create_objc_class, on_main_thread
from objc_util import c,sel, CGRect

import pdbg

# --- navigation
UINavigationController = ObjCClass('UINavigationController')
UINavigationBarAppearance = ObjCClass('UINavigationBarAppearance')
UIBarButtonItem = ObjCClass('UIBarButtonItem')

# --- viewController
UIViewController = ObjCClass('UIViewController')

# --- view
UIView = ObjCClass('UIView')
NSLayoutConstraint = ObjCClass('NSLayoutConstraint')

UIColor = ObjCClass('UIColor')

# --- Metal
MTKView = ObjCClass('MTKView')

MTLCreateSystemDefaultDevice = c.MTLCreateSystemDefaultDevice
MTLCreateSystemDefaultDevice.argtypes = []
MTLCreateSystemDefaultDevice.restype = ctypes.c_void_p




class AAPLRenderer:

  def __init__(self):
    self._device: 'MTLDevice'
    self._commandQueue: 'MTLCommandQueue'

  def create_delegate(self):
    # --- `MTKViewDelegate` Methods
    def initWithMetalKitView_(_self, _cmd, _mtkView):
      mtkView = ObjCInstance(_mtkView)


class AAPLViewController:

  def __init__(self):
    self._viewController: UIViewController
    self._view: MTKView
    self._renderer: AAPLRenderer

  def _override_viewController(self):

    # --- `UIViewController` Methods

    def viewDidLoad(_self, _cmd):
      #print('viewDidLoad')
      this = ObjCInstance(_self)
      view = this.view()
      pdbg.state(this)

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
    self.nav_title = 'nav title'
    self.sub_view = UIView.alloc()

  def setup_viewDidLoad(self, this: UIViewController):
    # xxx: `viewDidLoad` が肥大化しそうなので、レイアウト関係以外はこっちで処理

    # xxx: navigationItem 関係は、`UINavigationController` を`create_objc_class` して、navigation 側で処理してもいいかも
    # --- navigationItem
    navigationItem = this.navigationItem()
    navigationItem.setTitle_(self.nav_title)

    # --- view
    CGRectZero = CGRect((0.0, 0.0), (0.0, 0.0))
    self.sub_view.initWithFrame_(CGRectZero)
    self.sub_view.setBackgroundColor_(UIColor.systemRedColor())

  def _override_viewController(self):

    # --- `UIViewController` Methods
    def doneButtonTapped_(_self, _cmd, _sender):
      this = ObjCInstance(_self)
      this.dismissViewControllerAnimated_completion_(True, None)

    def viewDidLoad(_self, _cmd):
      #print('viewDidLoad')
      this = ObjCInstance(_self)
      self.setup_navigation(this)
      self.setup_viewDidLoad(this)
      view = this.view()

      # --- layout
      view.addSubview_(self.sub_view)
      self.sub_view.translatesAutoresizingMaskIntoConstraints = False

      NSLayoutConstraint.activateConstraints_([
        self.sub_view.centerXAnchor().constraintEqualToAnchor_(
          view.centerXAnchor()),
        self.sub_view.centerYAnchor().constraintEqualToAnchor_(
          view.centerYAnchor()),
        self.sub_view.widthAnchor().constraintEqualToAnchor_multiplier_(
          view.widthAnchor(), 0.9),
        self.sub_view.heightAnchor().constraintEqualToAnchor_multiplier_(
          view.heightAnchor(), 0.9),
      ])

    # --- `UIViewController` set up
    _methods = [
      doneButtonTapped_,
      viewDidLoad,
    ]

    create_kwargs = {
      'name': '_vc',
      'superclass': UIViewController,
      'methods': _methods,
    }
    _vc = create_objc_class(**create_kwargs)
    self._viewController = _vc

  def setup_navigation(self, this: UIViewController):
    this.setEdgesForExtendedLayout_(0)
    # todo: view 閉じる用の実装など
    navigationController = this.navigationController()
    navigationBar = navigationController.navigationBar()

    # --- appearance
    appearance = UINavigationBarAppearance.alloc()
    appearance.configureWithDefaultBackground()
    #appearance.configureWithOpaqueBackground()
    #appearance.configureWithTransparentBackground()

    # --- navigationBar
    navigationBar.standardAppearance = appearance
    navigationBar.scrollEdgeAppearance = appearance
    navigationBar.compactAppearance = appearance
    navigationBar.compactScrollEdgeAppearance = appearance

    #navigationBar.prefersLargeTitles = True

    done_btn = UIBarButtonItem.alloc(
    ).initWithBarButtonSystemItem_target_action_(0, this,
                                                 sel('doneButtonTapped:'))

    navigationItem = this.navigationItem()
    navigationItem.rightBarButtonItem = done_btn

  @on_main_thread
  def _init(self):
    self._override_viewController()
    vc = self._viewController.new().autorelease()
    nv = UINavigationController.alloc()
    nv.initWithRootViewController_(vc).autorelease()
    return nv

  @classmethod
  def new(cls) -> ObjCInstance:
    _cls = cls()
    return _cls._init()


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
  ovc = AAPLViewController.new()
  present_objc(ovc)

