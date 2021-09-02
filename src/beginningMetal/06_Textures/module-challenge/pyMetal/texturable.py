from pathlib import Path

from objc_util import ObjCClass, ns, nsurl

from .utils import err_ptr


class Texturable:
  def setTexture_device_imageName_(self, device, imageName):
    # xxx: Shader path もやる？
    def get_image_path(_imageName):
      root = Path('./Images')
      for file in root.iterdir():
        if file.name == _imageName:
          return file.absolute()

    textureLoader = ObjCClass('MTKTextureLoader').new()
    textureLoader.initWithDevice_(device)
    origin = 'MTKTextureLoaderOriginBottomLeft'
    textureLoaderOptions = ns({'MTKTextureLoaderOptionOrigin': origin})

    textureURL = nsurl(str(get_image_path(imageName)))
    texture = textureLoader.newTextureWithContentsOfURL_options_error_(
      textureURL, textureLoaderOptions, err_ptr)
    return texture

