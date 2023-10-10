import ctypes
from objc_util import ObjCClass, ObjCInstance, create_objc_class
from objc_util import c, on_main_thread, sel
import ui

import pdbg

# --- load objc classes
MTKView = ObjCClass('MTKView')

# --- navigation
UINavigationController = ObjCClass('UINavigationController')
UINavigationBarAppearance = ObjCClass('UINavigationBarAppearance')
UIBarButtonItem = ObjCClass('UIBarButtonItem')

# --- viewController
UIViewController = ObjCClass('UIViewController')

# --- view
NSLayoutConstraint = ObjCClass('NSLayoutConstraint')

UIColor = ObjCClass('UIColor')

# --- initialize MetalDevice
MTLCreateSystemDefaultDevice = c.MTLCreateSystemDefaultDevice
MTLCreateSystemDefaultDevice.argtypes = []
MTLCreateSystemDefaultDevice.restype = ctypes.c_void_p


class View(ui.View):

  def __init__(self, *args, **kwargs):
    ui.View.__init__(self, *args, **kwargs)
    self.bg_color = 'maroon'
    self.view_did_load()

  def view_did_load(self):
    mtkView = MTKView.alloc()
    _device = MTLCreateSystemDefaultDevice()

    devices = ObjCInstance(_device)
    mtkView.initWithFrame_device_(((0, 0), (100, 100)), devices)
    mtkView.setAutoresizingMask_((1 << 1) | (1 << 4))

    self.objc_instance.addSubview_(mtkView)


class ObjcUIViewController:

  def __init__(self):
    self._viewController: UIViewController

  def _override_viewController(self):

    # --- `UIViewController` Methods
    def doneButtonTapped_(_self, _cmd, _sender):
      this = ObjCInstance(_self)
      this.dismissViewControllerAnimated_completion_(True, None)

    def viewDidLoad(_self, _cmd):
      this = ObjCInstance(_self)
      self.setup_navigation(this)

    def didReceiveMemoryWarning(_self, _cmd):
      print('Dispose of any resources that can be recreated.')
      print('> 再作成可能なリソースは処分する。')

    # --- `UIViewController` set up
    _methods = [
      doneButtonTapped_,
      viewDidLoad,
      didReceiveMemoryWarning,
    ]

    create_kwargs = {
      'name': '_vc',
      'superclass': UIViewController,
      'methods': _methods,
    }
    _vc = create_objc_class(**create_kwargs)
    self._viewController = _vc

  def setup_navigation(self, this: UIViewController):
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
    #navigationController.setHidesBarsOnSwipe_(True)

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
  vc.setModalPresentationStyle(0)
  root_vc.presentViewController_animated_completion_(vc, True, None)


if __name__ == '__main__':
  ovc = ObjcUIViewController.new()
  present_objc(ovc)

