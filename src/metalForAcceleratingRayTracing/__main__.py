import ui

from gameViewController import GameViewController




class ViewController(ui.View):
  def __init__(self, *args, **kwargs):
    ui.View.__init__(self, *args, **kwargs)
    self.bg_color = 'slategray'
    #self.present(style='fullscreen', orientations=['portrait'])


if __name__ == '__main__':
  vc = ViewController()
  vc.present(style='fullscreen', orientations=['portrait'])

