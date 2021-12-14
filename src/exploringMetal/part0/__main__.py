import ui

from gameViewController import GameViewController


class MainView(ui.View):
  def __init__(self, *args, **kwargs):
    ui.View.__init__(self, *args, **kwargs)
    self.bg_color = 'slategray'
    #self.present(style='fullscreen', orientations=['portrait'])
    self.gvc = GameViewController()
    self.objc_instance.addSubview_(self.gvc.mtkView)


if __name__ == '__main__':
  main = MainView()
  main.present(style='fullscreen', orientations=['portrait'])

