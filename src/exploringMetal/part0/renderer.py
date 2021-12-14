import ctypes

from objc_util import create_objc_class, ObjCClass


class Renderer:
  def __init__(self, metalKitView):
    self.device = metalKitView.device()

  def renderer_init(self):
    def mtkView_drawableSizeWillChange_(_self, _cmd, _view, _size):
      print('mtkView_drawableSizeWillChange')

    def drawInMTKView_(_self, _cmd, _view):
      print('drawInMTKView')

    PyRenderer = create_objc_class(
      name='PyRenderer',
      methods=[drawInMTKView_, mtkView_drawableSizeWillChange_],
      protocols=['MTKViewDelegate'])
    return PyRenderer.new()


if __name__ == '__main__':
  from gameViewController import GameViewController
  gvc = GameViewController()
  Renderer(gvc.mtkView)

