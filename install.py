from utility import *

subvolume_mounts = {
    "@arch-root": "/mnt",
    "@arch-log": "/mnt/var/log",
}

def create_subvolumes(btrfs_partition, current_subvolumes):
    Command(f"mount {btrfs_partition} /mnt").run()
    for needed_subvolume in subvolume_mounts.keys():
        if needed_subvolume in current_subvolumes:
            Command(f"btrfs subvolume delete /mnt/{needed_subvolume}").run()
        Command(f"btrfs subvolume create /mnt/{needed_subvolume}").run()
    Command(f"umount /mnt").run()

def mount(efi_partition, btrfs_partition):
    for subvolume, mount in subvolume_mounts.items():
        Command(f"mount -o compress=zstd,subvol={subvolume} {btrfs_partition} {mount}").run()
    Command(f"mount --mkdir {efi_partition} /mnt/efi").run()

def main():
    disk = select_disk()
    efi_partition, btrfs_partition = list_partitions(disk)
    current_subvolumes = list_subvolumes()
    create_subvolumes(btrfs_partition, current_subvolumes)
    mount(efi_partition, btrfs_partition)

if __name__ == "__main__":
    main()