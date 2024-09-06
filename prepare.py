from utility import *

def partition(disk_name: str):
    gpt = Command(f"sgdisk -og {disk_name}")
    gpt.comment("Clear all partitions from disk")
    gpt.comment("Only do this if you are installing for the first time")
    gpt.comment("This will destroy data")
    gpt.confirm()

    efi = Command(f'sgdisk -n 1:0:+2GiB -c 1:"EFI-System-Partition" -t 1:ef00 {disk_name}')
    efi.comment("Create efi partition")
    efi.comment("Creates a 2GiB Partition at the first avaialable location")
    efi.confirm()

    btrfs = Command(f'sgdisk -n 2:0:0 -c 2:"BTRFS-Partition" -t 2:8300 {disk_name}')
    btrfs.comment("Create btrfs partition")
    btrfs.comment("Creates a btrfs partition with the rest of the disk")
    btrfs.confirm()

def format(efi_partition, btrfs_partition):
    efi = Command(f"mkfs.fat -F 32 {efi_partition}")
    efi.comment("Format the efi partition")
    efi.comment("This will destroy data")
    efi.confirm()

    btrfs = Command(f"mkfs.btrfs {btrfs_partition}")
    btrfs.comment("Format the btrfs partition")
    btrfs.comment("This will destroy data")
    btrfs.confirm() 

def subvolume(btrfs_partition: str):
    current_subvolumes = list_subvolumes(btrfs_partition)
    if "@my" not in current_subvolumes:
        Command(f"mount {btrfs_partition} /mnt").run()
        Command("btrfs subvolume create /mnt/@my").run()
        Command(f"umount /mnt").run()

def main():
    disk = select_disk()
    partition(disk)
    efi_partition, btrfs_partition = list_partitions(disk)
    format(efi_partition, btrfs_partition)
    subvolume(btrfs_partition)

if __name__ == "__main__":
    main()