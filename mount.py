from utility import *

subvolume_mounts = {
    "@arch-root": "/mnt",
    "@arch-log": "/mnt/var/log",
}

def create_subvolumes(btrfs_partition, current_subvolumes):
    Command(f"umount /mnt")
    Command(f"mount {btrfs_partition} /mnt")
    for needed_subvolume in subvolume_mounts.keys():
        if needed_subvolume in current_subvolumes:
            Command(f"btrfs subvolume delete /mnt/{needed_subvolume}")
        Command(f"btrfs subvolume create /mnt/{needed_subvolume}")
    Command(f"umount /mnt")

def mount(efi_partition, btrfs_partition):
    Command("umount /mnt/efi")
    Command("umount /mnt/var/log")
    Command("umount /mnt")
    for subvolume, mount in subvolume_mounts.items():
        Command(f"mount --mkdir -o compress=zstd,subvol={subvolume} {btrfs_partition} {mount}")
    Command(f"mount --mkdir {efi_partition} /mnt/efi")

def mount_my(btrfs_partition):
    Command(f"mount --mkdir -o compress=zstd,subvol=@my {btrfs_partition} /mnt/.my")

def genfstab():
    fstab = Command("genfstab -U /mnt").stdout
    write_file("/tmp/fstab", fstab)

def unmount_my():
    Command(f"umount /mnt/.my")

def main():
    Command("umount -R /mnt")
    disk = select_disk()
    efi_partition, btrfs_partition = list_partitions(disk)
    current_subvolumes = list_subvolumes(btrfs_partition)
    create_subvolumes(btrfs_partition, current_subvolumes)
    mount(efi_partition, btrfs_partition)
    mount_my(btrfs_partition)
    genfstab()
    unmount_my()


if __name__ == "__main__":
    main()