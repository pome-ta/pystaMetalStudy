from pathlib import Path
import ctypes

from objc_util import c, ObjCInstance

import pdbg

shader_path = Path('./Shaders.metal')

err_ptr = ctypes.c_void_p()


def MTLCreateSystemDefaultDevice():
  _MTLCreateSystemDefaultDevice = c.MTLCreateSystemDefaultDevice
  _MTLCreateSystemDefaultDevice.argtypes = []
  _MTLCreateSystemDefaultDevice.restype = ctypes.c_void_p
  return ObjCInstance(_MTLCreateSystemDefaultDevice())


device = MTLCreateSystemDefaultDevice()
source = shader_path.read_text('utf-8')

library = device.newLibraryWithSource(source, options=None, error=err_ptr)

for name in library.functionNames():
  function = library.newFunctionWithName(name)
  print(function)

