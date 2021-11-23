from objc_util import ObjCClass, ns, nsurl

from .utils import err_ptr, get_file_path


class Texturable:
  def setTexture_device_imageName_(self, device, imageName):

    if get_file_path(imageName):
      _url = get_file_path(imageName)
    else:
      return None

    textureLoader = ObjCClass('MTKTextureLoader').new()
    textureLoader.initWithDevice_(device)

    origin = 'MTKTextureLoaderOriginBottomLeft'
    textureLoaderOptions = ns({
      'MTKTextureLoaderOptionOrigin': origin,
      'MTKTextureLoaderOptionSRGB': 0
    })

    textureURL = nsurl(str(_url))
    texture = textureLoader.newTextureWithContentsOfURL_options_error_(
      textureURL, textureLoaderOptions, err_ptr)
    return texture

