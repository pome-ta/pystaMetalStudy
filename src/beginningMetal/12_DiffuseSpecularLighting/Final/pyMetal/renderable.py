from objc_util import ObjCClass

from .utils import err_ptr, get_file_path

shader_path = get_file_path('Shader.metal')


class Renderable:
  def doRender_commandEncoder_modelViewMatrix_(self, commandEncoder, modelViewMatrix):
    pass
  
  def buildPipelineState(self, device):
    source = shader_path.read_text('utf-8')
    MTLCompileOptions = ObjCClass('MTLCompileOptions')
    options = MTLCompileOptions.new()
    library = device.newLibraryWithSource_options_error_(
      source, options, err_ptr)
    
    vertexFunction = library.newFunctionWithName_(
      self.vertexFunctionName)
    fragmentFunction = library.newFunctionWithName_(
      self.fragmentFunctionName)
    
    rpld = ObjCClass('MTLRenderPipelineDescriptor').new()
    rpld.vertexFunction = vertexFunction
    rpld.fragmentFunction = fragmentFunction
    rpld.colorAttachments().objectAtIndexedSubscript_(
      0).pixelFormat = 80  # .bgra8Unorm
    
    rpld.depthAttachmentPixelFormat = 252  # .depth32Float
    rpld.vertexDescriptor = self.vertexDescriptor
    rps = device.newRenderPipelineStateWithDescriptor_error_(rpld, err_ptr)
    return rps
