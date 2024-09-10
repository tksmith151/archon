from namespace.standard import *

def partition(disk_name: str):  
    partitions = get_partitions(disk_name)
    if partitions:
        verify_partitions(disk_name)
        return
    # Create new gpt
    Command(f"sgdisk -a 2048 -o {disk_name}")
    # Create efi partition
    Command(f'sgdisk -n 1:0:+1GiB -c 1:"efi" -t 1:ef00 {disk_name}')
    # Create boot partition
    Command(f'sgdisk -n 2:0:+1GiB -c 2:"boot" -t 2:ef02 {disk_name}')
    # Create luks partition
    Command(f'sgdisk -n 3:0:0 -c 3:"luks" -t 3:8300 {disk_name}')
    # Verify partitions
    verify_partitions(disk_name)

def main():
    disk = select_disk()
    partition(disk)

if __name__ == "__main__":
    main()