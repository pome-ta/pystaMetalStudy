from objc_util import create_objc_class, ObjCClass, ObjCInstance

class Renderer:
  def __init__(self, device):
    self.device = device
    self.commandQueue = self.device.newCommandQueue()
    self.buildPipelineState()

  def buildPipelineState(self):
    descriptor = ObjCClass('MTLSamplerDescriptor').new()
    # nearest = 0
    # linear = 1
    descriptor.minFilter = 1
    descriptor.magFilter = 1
    self.samplerState = self.device.newSamplerStateWithDescriptor_(descriptor)

  def renderer_init(self, scene):
    self.scene = scene

    # todo: MTKViewDelegate func
    def mtkView_drawableSizeWillChange_(_self, _cmd, _view, _size):
      pass

    def drawInMTKView_(_self, _cmd, _view):
      view = ObjCInstance(_view)
      drawable = view.currentDrawable()
      rpd = view.currentRenderPassDescriptor()

      deltaTime = 1 / view.preferredFramesPerSecond()

      commandBuffer = self.commandQueue.commandBuffer()
      commandEncoder = commandBuffer.renderCommandEncoderWithDescriptor_(rpd)
      commandEncoder.setFragmentSamplerState_atIndex_(self.samplerState, 0)

      self.scene.render_commandEncoder_deltaTime_(commandEncoder, deltaTime)

      commandEncoder.endEncoding()
      commandBuffer.presentDrawable_(drawable)
      commandBuffer.commit()

    PyRenderer = create_objc_class(
      name='PyRenderer',
      methods=[drawInMTKView_, mtkView_drawableSizeWillChange_],
      protocols=['MTKViewDelegate'])
    return PyRenderer.new()


