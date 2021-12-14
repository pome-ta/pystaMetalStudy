from pathlib import Path
import ctypes

from objc_util import create_objc_class, ObjCClass, ObjCInstance

root_path = Path(__file__).parent
header_path = root_path / Path('./ShaderTypes.h')
shader_path = root_path / Path('./Shaders.metal')

err_ptr = ctypes.c_void_p()


class Renderer:
  def __init__(self, metalKitView):
    self.vertexArray = (ctypes.c_float * 24)(0.5, -0.5, 1.0, 0.0, 0.0, 1.0,
                                             -0.5, -0.5, 0.0, 1.0, 0.0, 1.0,
                                             0.0, 0.5, 0.0, 0.0, 1.0, 1.0)
    self.device = metalKitView.device()

    # --- load shader code
    header = header_path.read_text('utf-8')
    shader = shader_path.read_text('utf-8')
    #source = header + shader
    source = shader
    library = self.device.newLibraryWithSource_options_error_(
      source, err_ptr, err_ptr)

    vertexFunction = library.newFunctionWithName_('helloVertexShader')
    fragmentFunction = library.newFunctionWithName_('helloFragmentShader')

    pipelineDescriptor = ObjCClass('MTLRenderPipelineDescriptor').new()
    pipelineDescriptor.vertexFunction = vertexFunction
    pipelineDescriptor.fragmentFunction = fragmentFunction
    pipelineDescriptor.colorAttachments().objectAtIndexedSubscript_(
      0).pixelFormat = 80  # .bgra8Unorm

    self.pipelineState = self.device.newRenderPipelineStateWithDescriptor_error_(
      pipelineDescriptor, err_ptr)

    self.commandQueue = self.device.newCommandQueue()

  def renderer_init(self):
    def mtkView_drawableSizeWillChange_(_self, _cmd, _view, _size):
      print('mtkView_drawableSizeWillChange')

    def drawInMTKView_(_self, _cmd, _view):
      #print('drawInMTKView')
      view = ObjCInstance(_view)
      commandBuffer = self.commandQueue.commandBuffer()
      tempRenderPassDescriptor = view.currentRenderPassDescriptor()

      if tempRenderPassDescriptor:
        renderPassDescriptor = tempRenderPassDescriptor
        renderPassDescriptor.colorAttachments().objectAtIndexedSubscript_(
          0).clearColor = (0.0, 0.0, 0.0, 1.0)
        renderPassDescriptor.colorAttachments().objectAtIndexedSubscript_(
          0).loadAction = 2  # MTLLoadActionClear .clear
        renderEncoder = commandBuffer.renderCommandEncoderWithDescriptor_(
          renderPassDescriptor)

        renderEncoder.setVertexBytes_length_atIndex_(
          self.vertexArray, ctypes.sizeof(self.vertexArray), 0)
        renderEncoder.setRenderPipelineState_(self.pipelineState)
        renderEncoder.drawPrimitives_vertexStart_vertexCount_(3, 0, 3)
        renderEncoder.endEncoding()
        commandBuffer.presentDrawable_(view.currentDrawable())
      commandBuffer.commit()

    PyRenderer = create_objc_class(
      name='PyRenderer',
      methods=[drawInMTKView_, mtkView_drawableSizeWillChange_],
      protocols=['MTKViewDelegate'])
    return PyRenderer.new()


if __name__ == '__main__':
  from gameViewController import GameViewController
  gvc = GameViewController()
  Renderer(gvc.mtkView)

