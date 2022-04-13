import ui

from pyMetal import MetalView


class ViewController(ui.View):
  def __init__(self, *args, **kwargs):
    ui.View.__init__(self, *args, **kwargs)
    self.bg_color = 'slategray'
    # todo: touch 判明用
    self.oval = ui.View()
    self.oval.bg_color = 'maroon'
    self.oval.corner_radius = 48
    self.oval.alpha = 0.0

    # self.present(style='fullscreen', orientations=['portrait'])
    # self.present(style='fullscreen', orientations=['landscape'])
    self.present(style='fullscreen')

    _bounds = self.bounds
    self.metal = MetalView(_bounds)
    self.objc_instance.addSubview_(self.metal.mtkView)
    self.add_subview(self.oval)

  def touch_began(self, touch):
    self.metal.touch_began(touch)
    locate = touch.location
    self.oval.x = locate.x - (self.oval.width / 2)
    self.oval.y = locate.y - (self.oval.height / 2)
    self.oval.alpha = 0.3

  def touch_moved(self, touch):
    self.metal.touch_moved(touch)
    locate = touch.location
    self.oval.x = locate.x - (self.oval.width / 2)
    self.oval.y = locate.y - (self.oval.height / 2)
    self.oval.alpha = 0.6

  def touch_ended(self, touch):
    self.oval.alpha = 0.0


if __name__ == '__main__':
  view = ViewController()

