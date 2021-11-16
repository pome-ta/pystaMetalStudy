from pathlib import Path
import ctypes

err_ptr = ctypes.c_void_p()

path_list = Path.cwd().glob('./**')

def get_file_path(file_name):
  for file_path in path_list:
    for file in file_path.iterdir():
      if file.name == file_name:
        return file.absolute()
  return None
