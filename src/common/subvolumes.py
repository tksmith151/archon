from namespace.common import *

def unmount_all():
    mount_paths = [
        "/mnt/efi",
        "/mnt/boot",
        "/mnt/home",
        "/mnt/var/log",
        "/mnt/var/cache/pacman/pkg",
        "/mnt/.snapshots",
        "/mnt/my",
        "/mnt"
    ]
    for mount_path in mount_paths:
        if os.path.ismount(mount_path):
            Command(f"umount {mount_path}")

def list_subvolumes(btrfs_partition):
    unmount_all()
    Command(f"mount {btrfs_partition} /mnt")

    btrfs = Command(f"btrfs subvolume list -a /mnt", quiet=True)
    output = btrfs.stdout
    
    paths = set()
    lines = output.split("\n")
    for line in lines:
        fields = line.split(" ")
        path = fields[-1].split("/")[-1]
        if path:
            paths.add(path)

    unmount_all()

    return sorted(paths)