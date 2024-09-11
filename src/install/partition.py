from namespace.standard import *

def partition(disk_name: str):
    # Verify partitions if they already exist
    partitions = get_partitions(disk_name)
    if partitions:
        verify_partitions(disk_name)
        return
    # Create new gpt
    Command(f"sgdisk -a 2048 -o {disk_name}")
    # Create partitions
    boot_size = "2GiB"
    partitions = [
        f'-n 1:0:+{boot_size} -c 1:"efi" -t 1:ef00',
        f'-n 2:0:0 -c 2:"luks" -t 2:8300'
    ]
    Command(f'sgdisk {" ".join(partitions)} {disk_name}')