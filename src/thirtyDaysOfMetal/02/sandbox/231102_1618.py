import ctypes
import pdbg

i = ctypes.c_uint32(10)  # unsigned int i = 10;
f = ctypes.c_float(25.4)  # float = 25.4;

print(i.value)
print(f.value)

pdbg.state(i)
