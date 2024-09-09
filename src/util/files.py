from namespace.base import *

def copy_file(src, dst):
    shutil.copy(src, dst)

def write_file(location, data):
    with open(location, "w") as fd:
        fd.write(data)

def read_file(location):
    with open(location, "r") as fd:
        return fd.read()