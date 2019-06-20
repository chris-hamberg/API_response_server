import os, shutil


#NOTE dev tool for removing __pycache__ dirs
for root, directories, files in os.walk('../'):
    for directory in directories:
        if directory == "__pycache__":
            shutil.rmtree(os.path.join(root, directory))
