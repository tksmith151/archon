from utility import *

def list_disks():
    lsblk = Command()
    lsblk.set("lsblk --json")
    lsblk.run()
    disks: List[str] = []
    output: List[str] = []
    for device in json.loads(lsblk.stdout).get("blockdevices"):
        device_type = device.get("type")
        if device_type == "disk":
            device_name = device.get("name")
            device_size = device.get("size")
            disks.append(f"{device_name} - {device_size}")
            output.append(f"/dev/{device_name}")
    if not disks:
        raise Exception("No disks found")
    # display_lines(disks)
    return output

def partition(disk_name: str):
    gpt = Command()
    gpt.add("Clear all partitions from disk")
    gpt.add("Only do this if you are installing for the first time")
    gpt.set(f"sgdisk -og {disk_name}")
    gpt.confirm()

    efi = Command()
    efi.add("Create efi partition")
    efi.add("Creates a 2GiB Partition at the first avaialable location")
    efi.set(f'sgdisk -n 1:0:+2GiB -c 1:"EFI System Partition" -t 1:ef00 {disk_name}')
    gpt.confirm()

    btrfs = Command()
    btrfs.add("Create btrfs partition")
    btrfs.add("Creates a btrfs partition with the rest of the disk")
    btrfs.set(f'sgdisk -n 2:0:0 -c 2:"Linux LVM" -t 2:8300 {disk_name}')
    gpt.confirm()


def format(disk_name: str):
    efi = Command()
    efi.add("Format the efi partition")
    efi.set(f"mkfs.fat -F 32 {disk_name}p1")
    efi.confirm()

    btrfs = Command()
    btrfs.add("Format the btrfs partition")
    btrfs.set(f"mkfs.btrfs {disk_name}p2")
    btrfs.confirm()

def main():
    disks = list_disks()
    if len(disks) > 1:
        raise Exception("Too many disks")
    disk = disks[0]
    partition(disk)
    format(disk)

if __name__ == "__main__":
    main()