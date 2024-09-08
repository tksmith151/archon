from namespace.standard import *

def partition(disk_name: str):
    print("This action will wipe all partitions from the disk")
    print("and result in the loss of any existing data on the disk")
    confirmed = confirm(really=True)
    if not confirmed:
        return
    
    # Clear all partitions on disk
    Command(f"sfdisk --delete {disk_name}").run(show_progress=True)
    # Create new gpt
    Command(f"sgdisk -og {disk_name}").run(show_progress=True)
    # Create efi partition
    Command(f'sgdisk -n 1:0:+1GiB -c 1:"efi" -t 1:ef00 {disk_name}').run(show_progress=True)
    # Create boot partition
    Command(f'sgdisk -n 2:0:+1GiB -c 1:"boot" -t 1:ef02 {disk_name}').run(show_progress=True)
    # Create luks partition
    Command(f'sgdisk -n 3:0:0 -c 2:"luks" -t 2:8300 {disk_name}').run(show_progress=True)

    partitions = get_partitions()
    # Format efi partition
    Command(f"mkfs.fat -n efi -F 32 {partitions['efi']}").run(show_progress=True)
    # Format boot partition
    Command(f"mkfs.ext4 -L boot {partitions['boot']}")
    # Format luks partition
    # cryptsetup luksFormat
    # cryptsetup open --type luks
    Command(f"cryptsetup luksFormat {partitions['luks']}").run(show_progress=True)
    Command(f"cryptsetup open --type luks {partitions['luks']} btrfs").run(show_progress=True)
    btrfs_partition = "/dev/mapper/btrfs"
    Command(f"mkfs.btrfs {btrfs_partition}").run(show_progress=True)
    # Create my subvolume
    Command(f"mount {btrfs_partition} /mnt").run()
    Command("btrfs subvolume create /mnt/@my").run()
    Command(f"umount /mnt").run()

def main():
    disk = select_disk()
    partition(disk)

if __name__ == "__main__":
    main()