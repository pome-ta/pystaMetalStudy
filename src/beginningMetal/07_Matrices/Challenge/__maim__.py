import ui

from pyMetal import MetalView


class ViewController(ui.View):
  def __init__(self, *args, **kwargs):
    ui.View.__init__(self, *args, **kwargs)
    self.bg_color = 'slategray'
    self.present(style='fullscreen', orientations=['portrait'])

    _bounds = self.bounds
    self.metal = MetalView(_bounds)
    self.objc_instance.addSubview_(self.metal.mtkView)
    
    # --- print
    print('ViewController')


if __name__ == '__main__':
  view = ViewController()
