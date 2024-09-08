from namespace.common import *

def list_subvolumes(btrfs_partition):
    Command(f"umount /mnt").run()
    Command(f"mount {btrfs_partition} /mnt").run()

    btrfs = Command(f"btrfs subvolume list -a /mnt")
    btrfs.run()
    output = btrfs.stdout
    
    paths = set()
    lines = output.split("\n")
    for line in lines:
        fields = line.split(" ")
        path = fields[-1].split("/")[-1]
        if path:
            paths.add(path)

    Command(f"umount /mnt").run()

    return sorted(paths)