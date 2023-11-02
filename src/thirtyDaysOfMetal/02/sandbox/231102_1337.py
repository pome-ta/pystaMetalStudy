import ctypes
from objc_util import c, ObjCInstance

import pdbg


def MTLCreateSystemDefaultDevice():
  _MTLCreateSystemDefaultDevice = c.MTLCreateSystemDefaultDevice
  _MTLCreateSystemDefaultDevice.argtypes = []
  _MTLCreateSystemDefaultDevice.restype = ctypes.c_void_p
  return ObjCInstance(_MTLCreateSystemDefaultDevice())


device = MTLCreateSystemDefaultDevice()

buffer = device.newBufferWithLength(16, options=0)

#print(f'Buffer is {buffer.length()} bytes in length')
#pdbg.state(buffer)

contents = buffer.contents()
#pdbg.state(contents)
pdbg.state(buffer)

