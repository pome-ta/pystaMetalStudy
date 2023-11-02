import ctypes

#import numpy as np

from objc_util import c, ObjCInstance

import pdbg

#Float = np.dtype(np.float32, align=True)

#simd_float2 = ((ctypes.c_float * 2) * 2)()
points = ((ctypes.c_float * 2) * 2)()

#pdbg.state(points)


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
#pdbg.state(contents._objects)
#pdbg.state(buffer)
#p_c = ctypes.pointer(contents)
#print(dir(p_c))

#print(contents.value)

#ctypes.cast(points, ctypes.POINTER(contents))
#pdbg.state(contents.value)
print(contents)
a = ctypes.cast(contents, ctypes.POINTER(ctypes.c_float))
print(contents)

