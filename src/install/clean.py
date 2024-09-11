from namespace.standard import *

subvolume_mounts = {
    "@home": "/mnt/home",
    "@log": "/mnt/var/log",
    "@pkg": "/mnt/var/cache/pacman/pkg",
    "@.snapshots": "/mnt/.snapshots",
}

def clean(disk_name: str, system_password: str):
    btrfs_partition = "/dev/mapper/btrfs"
    partitions = get_partitions(disk_name)

    # Unlock luks if necessary
    if not os.path.exists(btrfs_partition):
        Command(f"cryptsetup open --type luks {partitions['luks']} btrfs")
    
    current_subvolumes = list_subvolumes(btrfs_partition)
    unmount_all()
    Command(f"mount {btrfs_partition} /mnt")
    if "@my" not in current_subvolumes:
        Command("btrfs subvolume create /mnt/@my")
    for current_subvolume in current_subvolumes:
        if current_subvolume == "@my":
            continue
        if current_subvolume == "@":
            continue
        Command(f"btrfs subvolume delete /mnt/{current_subvolume}")
    if "@" in current_subvolumes:
        Command(f"btrfs subvolume delete /mnt/@")
    Command(f"btrfs subvolume create /mnt/@")
    for needed_subvolume in subvolume_mounts.keys():
        Command(f"btrfs subvolume create /mnt/{needed_subvolume}")



def main():
    disk = select_disk()
    clean(disk)
    


if __name__ == "__main__":
    main()