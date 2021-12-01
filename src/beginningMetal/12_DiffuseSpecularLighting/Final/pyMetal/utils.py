import ctypes
from pathlib import Path

err_ptr = ctypes.c_void_p()


def get_file_path(file_name):
  for file_path in Path.cwd().glob('./**'):
    for file in file_path.iterdir():
      if file.name == file_name:
        return file.absolute()
  return None
