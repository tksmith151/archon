from namespace.standard import *

def partition(disk_name: str):
    print("This action will wipe all partitions from the disk")
    print("and result in the loss of any existing data on the disk")
    confirmed = confirm(really=True)
    if not confirmed:
        return
    
    # Clear all partitions on disk
    Command(f"sfdisk --delete {disk_name}")
    # Create new gpt
    Command(f"sgdisk -og {disk_name}")
    # Create efi partition
    Command(f'sgdisk -n 1:0:+1GiB -c 1:"efi" -t 1:ef00 {disk_name}')
    # Create boot partition
    Command(f'sgdisk -n 2:0:+1GiB -c 2:"boot" -t 2:ef02 {disk_name}')
    # Create luks partition
    Command(f'sgdisk -n 3:0:0 -c 3:"luks" -t 3:8300 {disk_name}')

    partitions = get_partitions(disk_name)
    # Format efi partition
    Command(f"mkfs.fat -F 32 {partitions['efi']}")
    # Format boot partition
    Command(f"mkfs.ext4 {partitions['boot']}")
    # Format luks partition
    # cryptsetup luksFormat
    # cryptsetup open --type luks
    Command(f"cryptsetup --batch-mode --verify-passphrase luksFormat {partitions['luks']}", capture=False)
    Command(f"cryptsetup open --type luks {partitions['luks']} btrfs")
    # Format btrfs mapping
    btrfs_partition = "/dev/mapper/btrfs"
    Command(f"mkfs.btrfs -f {btrfs_partition}")

def main():
    disk = select_disk()
    partition(disk)

if __name__ == "__main__":
    main()