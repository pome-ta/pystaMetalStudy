from pathlib import Path
import ctypes

from objc_util import c, ObjCInstance

import pdbg

shader_path = Path('./Shaders.metal')

err_ptr = ctypes.c_void_p()

MTLStorageModeShared = 0
MTLResourceStorageModeShift = 4
MTLResourceStorageModeShared = MTLStorageModeShared << MTLResourceStorageModeShift


def MTLCreateSystemDefaultDevice():
  _MTLCreateSystemDefaultDevice = c.MTLCreateSystemDefaultDevice
  _MTLCreateSystemDefaultDevice.argtypes = []
  _MTLCreateSystemDefaultDevice.restype = ctypes.c_void_p
  return ObjCInstance(_MTLCreateSystemDefaultDevice())


device = MTLCreateSystemDefaultDevice()
commandQueue = device.newCommandQueue()

source = shader_path.read_text('utf-8')
library = device.newLibraryWithSource(source, options=None, error=err_ptr)

kernelFunction = library.newFunctionWithName('add_two_values')

computePipeline = device.newComputePipelineStateWithFunction(kernelFunction,
                                                             error=err_ptr)

elementCount = 256

# MemoryLayout<Float>.stride = 4
inputBufferA = device.newBufferWithLength(4 * elementCount,
                                          options=MTLResourceStorageModeShared)
inputBufferB = device.newBufferWithLength(4 * elementCount,
                                          options=MTLResourceStorageModeShared)
outputBuffer = device.newBufferWithLength(4 * elementCount,
                                          options=MTLResourceStorageModeShared)

pdbg.state(inputBufferA.contents())

