from pathlib import Path
import ctypes

from objc_util import ObjCClass

import pdbg


root_path = Path(__file__).parent
header_path = root_path / Path('./ShaderTypes.h')
shader_path = root_path / Path('./Shaders.metal')

err_ptr = ctypes.c_void_p()
MTLPixelFormatRGBA16Float = 115

class Renderer:
  def __init__(self):
    self.view: MTKView
    self.device: MTLDevice
    self.queue: MTLCommandQueue
    self.library: MTLLibrary

    self.accelerationStructure: MPSTriangleAccelerationStructure
    self.intersector: MPSRayIntersector

  def initWithMetalKitView_(self, _view):
    self.view = _view
    self.device = self.view.device()
    print(f'Metal device: {self.device.name()}')
    
    self.loadMetal()
    self.createPipelines()
    
  def loadMetal(self):
    self.view.colorPixelFormat = MTLPixelFormatRGBA16Float
    self.view.sampleCount = 1
    # xxx: size?
    self.view.drawableSize = self.view.frame().size
    
    # --- load shader code
    header = header_path.read_text('utf-8')
    shader = shader_path.read_text('utf-8')
    source = header + shader
    
    MTLCompileOptions = ObjCClass('MTLCompileOptions')
    options = MTLCompileOptions.new()
    self.library = self.device.newLibraryWithSource_options_error_(source, options, err_ptr)
    
    self.queue = self.device.newCommandQueue()
    
  def createPipelines(self):
    computeDescriptor = ObjCClass('MTLComputePipelineDescriptor').alloc().init()
    
    computeDescriptor.threadGroupSizeIsMultipleOfThreadExecutionWidth = 1
    
    rayKernel = self.library.newFunctionWithName_('rayKernel')
    computeDescriptor.computeFunction = rayKernel
    
    


if __name__ == '__main__':
  from gameViewController import GameViewController
  gv = GameViewController()
  #render = Renderer()
  
  #render.initWithMetalKitView_(gv.view)

