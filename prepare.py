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
    efi.confirm()

    btrfs = Command()
    btrfs.add("Create btrfs partition")
    btrfs.add("Creates a btrfs partition with the rest of the disk")
    btrfs.set(f'sgdisk -n 2:0:0 -c 2:"BTRFS Partition" -t 2:8300 {disk_name}')
    btrfs.confirm()

def list_partitions(disk_name):
    disk_name
    lsblk = Command()
    lsblk.set(f"lsblk --json {disk_name}")
    lsblk.run()
    efi_partition = None
    btrfs_partition = None
    drive = json.loads(lsblk.stdout).get("blockdevices")[0]
    partitions = drive["children"]
    if len(partitions) != 2:
        raise Exception("Incorrect number of partitions")
    for partition in drive["children"]:
        partition_type = partition["type"]
        if partition_type != "part":
            continue
        partition_name = partition["name"]
        if partition["size"] == "2G":
            efi_partition = f"/dev/{partition_name}"
        else:
            btrfs_partition = f"/dev/{partition_name}"
    return efi_partition, btrfs_partition

def format(efi_partition, btrfs_partition):
    efi = Command()
    efi.add("Format the efi partition")
    efi.set(f"mkfs.fat -F 32 {efi_partition}")
    efi.confirm()

    btrfs = Command()
    btrfs.add("Format the btrfs partition")
    btrfs.set(f"mkfs.btrfs {btrfs_partition}")
    btrfs.confirm() 

def subvolume(btrfs_partition: str):
    mount = Command()
    mount.set(f"mount {btrfs_partition} /mnt")
    mount.run()

    root = Command()
    root.add("Add root btrfs subvolume")
    root.set("btrfs subvolume create /mnt/@")
    root.confirm()

    umount = Command()
    umount.set(f"umount /mnt")
    umount.run()

def main():
    disks = list_disks()
    if len(disks) > 1:
        raise Exception("Too many disks")
    disk = disks[0]
    partition(disk)
    efi_partition, btrfs_partition = list_partitions(disk)
    format(efi_partition, btrfs_partition)
    subvolume(btrfs_partition)

if __name__ == "__main__":
    main()