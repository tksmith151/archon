from namespace.standard import *

def format(disk_name: str):
    partitions = get_partitions(disk_name)
    # Format efi partition
    Command(f"mkfs.fat -F 32 {partitions['efi']}")
    # Format boot partition
    Command(f"mkfs.ext4 {partitions['boot']}")
    # Format luks partition
    Command(f"cryptsetup --batch-mode --verify-passphrase luksFormat {partitions['luks']}", capture=False)
    Command(f"cryptsetup open --type luks {partitions['luks']} btrfs")
    # Format btrfs mapping
    btrfs_partition = "/dev/mapper/btrfs"
    Command(f"mkfs.btrfs -f {btrfs_partition}")

def main():
    disk = select_disk()
    format(disk)

if __name__ == "__main__":
    main()