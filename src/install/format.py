from namespace.standard import *

def format(disk_name: str):
    partitions = get_partitions(disk_name)
    # Format efi partition
    efi_partition = partitions['efi']
    if get_filesystem_type(efi_partition) is None:
        Command(f"mkfs.fat -F 32 {efi_partition}")
    # Format boot partition
    boot_partition = partitions['boot']
    if get_filesystem_type(boot_partition) is None:
        Command(f"mkfs.ext4 {boot_partition}")
    # Format luks partition
    luks_partition = partitions['luks']
    if get_filesystem_type(luks_partition) is None:
        Command(f"cryptsetup --batch-mode --verify-passphrase luksFormat {luks_partition}", capture=False)
    
    btrfs_partition = "/dev/mapper/btrfs"
    if not os.path.exists(btrfs_partition):
        Command(f"cryptsetup open --type luks {luks_partition} btrfs")

    # Format btrfs mapping
    if get_filesystem_type(btrfs_partition) is None:
        Command(f"mkfs.btrfs -f {btrfs_partition}")

    # TODO: Verify file system types

def main():
    disk = select_disk()
    format(disk)

if __name__ == "__main__":
    main()