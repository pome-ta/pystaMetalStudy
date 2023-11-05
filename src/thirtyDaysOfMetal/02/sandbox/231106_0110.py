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

buffer = device.newBufferWithBytes(bytes,
                                   length=ctypes.sizeof(bytes),
                                   options=0)

#print(f'Buffer is {buffer.length()} bytes in length')

contents = buffer.contents()
pdbg.state(contents)
#print(ObjCInstance(contents))
#pdbg.state(contents._objects)
#pdbg.state(buffer)
#p_c = ctypes.pointer(contents)
#print(dir(p_c))

#print(contents.value)

#ctypes.cast(points, ctypes.POINTER(contents))
#pdbg.state(contents.value)
#print(dir(contents))
#a = ctypes.cast(contents, ctypes.POINTER(ctypes.c_float))
#print(contents)

#print(dir(bytes))
print(bytes.__sizeof__())
print(ctypes.sizeof(bytes))

