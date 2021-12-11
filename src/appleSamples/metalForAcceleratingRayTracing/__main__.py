import ui

from gameViewController import GameViewController




class ViewController(ui.View):
  def __init__(self, *args, **kwargs):
    ui.View.__init__(self, *args, **kwargs)
    self.bg_color = 'slategray'
    #self.present(style='fullscreen', orientations=['portrait'])
    gv = GameViewController()
    self.objc_instance.addSubview_(gv.view)


if __name__ == '__main__':
  vc = ViewController()
  vc.present(style='fullscreen', orientations=['portrait'])

