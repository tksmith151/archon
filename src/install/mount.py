from namespace.standard import *

subvolume_mounts = {
    "@home": "/mnt/home",
    "@log": "/mnt/var/log",
    "@pkg": "/mnt/var/cache/pacman/pkg",
    "@.snapshots": "/mnt/.snapshots",
}

def mount(disk_name: str):
    btrfs_partition = "/dev/mapper/btrfs"
    partitions = get_partitions(disk_name)

    # Unlock luks if necessary
    if not os.path.exists(btrfs_partition):
        Command(f"cryptsetup open --type luks {partitions['luks']} btrfs")

    # Clean mounts
    unmount_all()

    # Mount btrfs arch subvolumes
    Command(f"mount -o compress=zstd,subvol=@ {btrfs_partition} /mnt")
    for subvolume, mount in subvolume_mounts.items():
        os.makedirs(mount, exist_ok=True)
        Command(f"mount -o compress=zstd,subvol={subvolume} {btrfs_partition} {mount}")

    # Mount boot
    os.makedirs("/mnt/boot", exist_ok=True)
    Command(f"mount {partitions['boot']} /mnt/boot")

    # Mount @my
    os.makedirs("/mnt/my", exist_ok=True)
    Command(f"mount -o compress=zstd,subvol=@my {btrfs_partition} /mnt/my")

    # Generate fstab
    fstab = Command("genfstab -U /mnt", quiet=True).stdout
    write_file("/tmp/fstab", fstab)

    # Mount efi after generating fstab
    os.makedirs("/mnt/efi", exist_ok=True)
    Command(f"mount {partitions['efi']} /mnt/efi")



def main():
    disk = select_disk()
    mount(disk)
    


if __name__ == "__main__":
    main()