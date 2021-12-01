from objc_util import create_objc_class, ObjCClass, ObjCInstance


class Renderer:
  def __init__(self, device):
    self.device = device
    self.commandQueue = self.device.newCommandQueue()
    self.buildPipelineState()
    self.buildDepthStencilState()
  
  def buildPipelineState(self):
    descriptor = ObjCClass('MTLSamplerDescriptor').new()
    descriptor.minFilter = 1
    descriptor.magFilter = 1
    self.samplerState = self.device.newSamplerStateWithDescriptor_(descriptor)
  
  def buildDepthStencilState(self):
    depthStencilDescriptor = ObjCClass('MTLDepthStencilDescriptor').new()
    depthStencilDescriptor.setDepthCompareFunction_(1)  # .less
    depthStencilDescriptor.setDepthWriteEnabled_(1)  # true
    self.depthStencilState = self.device.newDepthStencilStateWithDescriptor_(
      depthStencilDescriptor)
  
  def renderer_init(self, scene):
    self.scene = scene
    
    # todo: MTKViewDelegate func
    def mtkView_drawableSizeWillChange_(_self, _cmd, _view, _size):
      view = ObjCInstance(_view)
      size = [view.size().width, view.size().height]
      self.scene.sceneSizeWillChange_size_(size)
    
    def drawInMTKView_(_self, _cmd, _view):
      view = ObjCInstance(_view)
      drawable = view.currentDrawable()
      rpd = view.currentRenderPassDescriptor()
      
      deltaTime = 1 / view.preferredFramesPerSecond()
      
      commandBuffer = self.commandQueue.commandBuffer()
      commandEncoder = commandBuffer.renderCommandEncoderWithDescriptor_(
        rpd)
      commandEncoder.setFragmentSamplerState_atIndex_(
        self.samplerState, 0)
      
      commandEncoder.setDepthStencilState_(
        self.depthStencilState)
      self.scene.render_commandEncoder_deltaTime_(
        commandEncoder, deltaTime)
      
      commandEncoder.endEncoding()
      commandBuffer.presentDrawable_(drawable)
      commandBuffer.commit()
    
    PyRenderer = create_objc_class(
      name='PyRenderer',
      methods=[drawInMTKView_, mtkView_drawableSizeWillChange_],
      protocols=['MTKViewDelegate'])
    return PyRenderer.new()
