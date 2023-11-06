import ctypes
from objc_util import c, ObjCInstance

import pdbg


def MTLCreateSystemDefaultDevice():
  _MTLCreateSystemDefaultDevice = c.MTLCreateSystemDefaultDevice
  _MTLCreateSystemDefaultDevice.argtypes = []
  _MTLCreateSystemDefaultDevice.restype = ctypes.c_void_p
  return ObjCInstance(_MTLCreateSystemDefaultDevice())


device = MTLCreateSystemDefaultDevice()

bytes = ((ctypes.c_float * 2) * 2)()

buffer = device.newBufferWithBytes(bytes, length=ctypes.sizeof(bytes), options=0)  # yapf: disable
buffer = device.newBufferWithLength(16, options=0)

print(f'Buffer is {buffer.length()} bytes in length')

contents = buffer.contents()
print(buffer.accelerationStructureUniqueIdentifier())
pdbg.state(buffer)

