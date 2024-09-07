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
    Command(f'sgdisk -n 2:0:+1GiB -c 1:"boot" -t 1:ef00 {disk_name}').run(show_progress=True)
    # Create luks partition
    Command(f'sgdisk -n 3:0:0 -c 2:"luks" -t 2:8300 {disk_name}').run(show_progress=True)


def main():
    disk = select_disk()
    partition(disk)

if __name__ == "__main__":
    main()