import numpy as np

vector_float4 = np.dtype(
  {
    'names': [
      'x',
      'y',
      'z',
      'w',
    ],
    'formats': [
      np.float32,
      np.float32,
      np.float32,
      np.float32,
    ],
    'offsets': [o * 4 for o in range(4)],
    'itemsize': 16,
  },
  align=True)

Vertex = np.dtype(
  {
    'names': [
      'position',
      'color',
    ],
    'formats': [
      vector_float4,
      vector_float4,
    ],
    'offsets': [0, 16],
  },
  align=True)

_v = [((-0.5, -0.5, 0.0, 1.0), (1, 0, 0, 1)),
      ((0.5, -0.5, 0.0, 1.0), (0, 1, 0, 1)),
      ((0.0, 0.5, 0.0, 1.0), (0, 0, 1, 1))]

vertexData = np.array((
  np.array(((-0.5, -0.5, 0.0, 1.0), (1, 0, 0, 1)), dtype=Vertex),
  np.array(((0.5, -0.5, 0.0, 1.0), (0, 1, 0, 1)), dtype=Vertex),
  np.array(((0.0, 0.5, 0.0, 1.0), (0, 0, 1, 1)), dtype=Vertex),
))

#vertexData = np.array(_v,dtype=Vertex)

a, *_ = vertexData.strides

print(vertexData)
print(vertexData.itemsize)
print(vertexData.shape)
print(vertexData.strides)

