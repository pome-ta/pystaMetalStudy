def add_arrays(inA: float, inB: float, result: float, length: int) -> None:
  for index in range(length):
    result[index] = inA[index] + inB[index]
