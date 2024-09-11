from namespace.standard import *

subvolume_mounts = {
    "@home": "/mnt/home",
    "@log": "/mnt/var/log",
    "@pkg": "/mnt/var/cache/pacman/pkg",
    "@.snapshots": "/mnt/.snapshots",
}

def mount(disk_name: str, system_password: str):
    partitions = get_partitions(disk_name)

    # Unlock luks if necessary
    if not os.path.exists(PATH.btrfs_partition):
        Command(f"cryptsetup open --type luks {partitions['luks']} btrfs")

    # Clean mounts
    unmount_all()

    # Mount btrfs arch subvolumes
    Command(f"mount -o compress=zstd,subvol=@ {PATH.btrfs_partition} /mnt")
    for subvolume, mount in subvolume_mounts.items():
        os.makedirs(mount, exist_ok=True)
        Command(f"mount -o compress=zstd,subvol={subvolume} {PATH.btrfs_partition} {mount}")

    # Mount @my
    os.makedirs("/mnt/my", exist_ok=True)
    Command(f"mount -o compress=zstd,subvol=@my {PATH.btrfs_partition} /mnt/my")

    # Mount efi
    os.makedirs("/mnt/boot", exist_ok=True)
    Command(f"mount {partitions['efi']} /mnt/boot")

    # Generate fstab
    fstab = Command("genfstab -U /mnt", quiet=True).stdout
    write_file("/tmp/fstab", fstab)



def main():
    disk = select_disk()
    mount(disk)
    


if __name__ == "__main__":
    main()