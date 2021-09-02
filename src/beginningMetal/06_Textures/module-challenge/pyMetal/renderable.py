from pathlib import Path

from objc_util import ObjCClass

from .utils import err_ptr


# xxx: shader path
shader_path = Path('./Shader.metal')

class Renderable:
  def buildPipelineState(self, device):
    source = shader_path.read_text('utf-8')
    library = device.newLibraryWithSource_options_error_(
      source, err_ptr, err_ptr)

    vertexFunction = library.newFunctionWithName_(self.vertexFunctionName)
    fragmentFunction = library.newFunctionWithName_(self.fragmentFunctionName)

    rpld = ObjCClass('MTLRenderPipelineDescriptor').new()
    rpld.vertexFunction = vertexFunction
    rpld.fragmentFunction = fragmentFunction
    rpld.colorAttachments().objectAtIndexedSubscript(
      0).pixelFormat = 80  # .bgra8Unorm

    rpld.vertexDescriptor = self.vertexDescriptor
    rps = device.newRenderPipelineStateWithDescriptor_error_(rpld, err_ptr)
    return rps

