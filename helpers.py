def isfile(file_name):
  full_file_path = "/".join((file_manager_directory, file_name))
  return os.path.isfile(full_file_path)

def isdir(dir_name):
  full_dir_path = "/".join((file_manager_directory, dir_name))
  return os.path.isdir(full_dir_path)
