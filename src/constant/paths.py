import pathlib

class Paths:
    def __init__(self):
        self.archon_dir = pathlib.Path(__file__).parent.parent.parent.resolve()
        self.btrfs_partition = "/dev/mapper/btrfs"

PATH = Paths()