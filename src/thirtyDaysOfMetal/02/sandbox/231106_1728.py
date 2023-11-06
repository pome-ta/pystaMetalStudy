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
bytes[0] = (10.0, 2.0)
bytes[1] = (20.0, 5.0)

buffer = device.newBufferWithBytes(bytes, length=ctypes.sizeof(bytes), options=0)  # yapf: disable
#buffer = device.newBufferWithLength(16, options=0)

#print(f'Buffer is {buffer.length()} bytes in length')

contents = buffer.contents()
#print(buffer.accelerationStructureUniqueIdentifier())
#pdbg.state(buffer.backingResource())
#pdbg.state(buffer.iosurface())

#pdbg.state(buffer.mutableCopy())

#print(buffer.allocatedSize())

#pdbg.state(contents)
#print(contents.value)
pdbg.state(buffer)
