import ctypes
import numpy as np

ext_vector_type = [('f', np.float32)]

position = np.array([-0.5, -0.5, 0.0, 1.0], dtype=ext_vector_type)

