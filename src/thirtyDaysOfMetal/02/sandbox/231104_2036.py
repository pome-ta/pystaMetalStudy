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
  funcPtr = _MTLCreateSystemDefaultDevice()
  return ObjCInstance(funcPtr)


device = MTLCreateSystemDefaultDevice()

buffer = device.newBufferWithLength(4, options=0)

#print(f'Buffer is {buffer.length()} bytes in length')
#pdbg.state(buffer)

contents = buffer.contents()


#print(dir(contents))
#print(contents.__sizeof__())
#print(contents.value)
'''
ptr = ctypes.pointer(contents)
#print(dir(ptr))
print(ptr.contents)
print(ctypes.sizeof(ptr))
p=ctypes.py_object(contents)

'''







#pdbg.state(contents)
#pdbg.state(contents.from_param())
#print(ObjCInstance(contents))
#pdbg.state(contents._objects)
#pdbg.state(buffer)
#p_c = ctypes.pointer(contents)
#print(dir(p_c))

#print(contents.value)
#pdbg.state(ObjCInstance(contents.value))

#ctypes.cast(points, ctypes.POINTER(contents))
#pdbg.state(contents.value)
#print(dir(contents))
#a = ctypes.cast(contents, ctypes.POINTER(ctypes.c_float))
#print(contents)

#print(ctypes.addressof(contents))
#print(ctypes.sizeof(contents))

