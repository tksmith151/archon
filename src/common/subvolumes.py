from namespace.common import *

def unmount_all():
    Command("umount -A --recursive /mnt", quiet=True, supress=True)

def list_subvolumes(btrfs_partition):
    unmount_all()
    Command(f"mount {btrfs_partition} /mnt")

    btrfs = Command(f"btrfs subvolume list -a /mnt", quiet=True)
    output = btrfs.stdout
    
    paths = set()
    lines = output.split("\n")
    for line in lines:
        fields = line.split(" ")
        path = fields[-1].replace("<FS_TREE>/","")
        if path:
            paths.add(path)

    unmount_all()

    return sorted(paths)