from utility import *

subvolume_mounts = {
    "@arch-root": "/mnt",
    "@arch-log": "/mnt/var/log",
}

def create_subvolumes(btrfs_partition, current_subvolumes):
    Command(f"umount /mnt").run()
    Command(f"mount {btrfs_partition} /mnt").run()
    for needed_subvolume in subvolume_mounts.keys():
        if needed_subvolume in current_subvolumes:
            Command(f"btrfs subvolume delete /mnt/{needed_subvolume}").run()
        Command(f"btrfs subvolume create /mnt/{needed_subvolume}").run()
    Command(f"umount /mnt").run()

def mount(efi_partition, btrfs_partition):
    Command("umount /mnt/efi").run()
    Command("umount /mnt/var/log").run()
    Command("umount /mnt").run()
    for subvolume, mount in subvolume_mounts.items():
        Command(f"mount --mkdir -o compress=zstd,subvol={subvolume} {btrfs_partition} {mount}").run()
    Command(f"mount --mkdir {efi_partition} /mnt/efi").run()

def mount_my(btrfs_partition):
    Command(f"mount --mkdir -o compress=zstd,subvol=@my {btrfs_partition} /mnt/.my").run()

def genfstab():
    Command("genfstab -U /mnt >> /tmp/fstab").run()

def unmount_my():
    Command(f"umount /mnt/.my").run()

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