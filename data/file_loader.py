import os

def get_file_paths(directory_path):
    file_paths = [os.path.join(directory_path, filename) 
                  for filename in os.listdir(directory_path) 
                  if filename.endswith('.xls')]
    return file_paths