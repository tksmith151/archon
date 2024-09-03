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
    display_lines(disks)
    return output

def partition(disk_name: str):
    efi = Command()
    efi.add("Create efi partition")
    efi.set(f"parted -s {disk_name} mklabel gpt mkpart primary ext4 0% 2GiB set 1 boot on")
    efi.show_summary()

    btrfs = Command()
    btrfs.add("Create btrfs partition")
    btrfs.set(f"parted -s {disk_name} mklabel msdos mkpart primary ext4 0% 2GiB set 1 boot on")
    btrfs.show_summary()


def format(disk_name: str):
    efi = Command()
    efi.set(f"mkfs.fat -F 32 {disk_name}p1")
    efi.show_summary()

    btrfs = Command()
    btrfs.set(f"mkfs.btrfs {disk_name}p2")
    btrfs.show_summary()

def main():
    disks = list_disks()
    if len(disks) > 1:
        raise Exception("Too many disks")
    disk = disks[0]
    partition(disk)
    format(disk)

if __name__ == "__main__":
    main()