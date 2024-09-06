import json
import shlex
import subprocess
from typing import List

def display_lines(lines: List[str]):
    for line in lines:
        print(line)

class Command:
    def __init__(self, string: str = None) -> None:
        self._string: str = string
        self._description: List[str] = []
        self._result = None

    def comment(self, description: str):
        self._description.append(f"# {description}")

    def show_summary(self):
        display_lines(self._description)
        print(self._string)
        print()

    def confirm(self):
        confirmed = False
        self.show_summary()
        confirmed = input("Perform above command (y/N):")
        if confirmed == "y":
            self.run()
            print(self.stderr)
            print(self.stdout)
            print()
            return confirmed
        print()
        return confirmed



    def run(self):
        if not self._result:
            result = subprocess.run(shlex.split(self._string), capture_output=True, text=True)
            self._result = result
            return
        raise Exception("Cannot run a command twice")
    
    @property
    def stdout(self):
        output: str = self._result.stdout
        return output
    
    @property
    def stderr(self):
        output: str = self._result.stderr
        return output

def select_disk():
    disks = list_disks()

def list_disks():
    lsblk = Command("lsblk --json")
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

def select_disk():
    output = None
    while output is None:
        disks = list_disks()
        print("Disks:")
        for index, disk in enumerate(disks):
            print(index, disk)
        disk_index = input("Select disk by index")
        try:
            disk = disks[disk_index]
            output = disk
        except:
            print("Invalid disk index")
        print()
    return output


def list_partitions(disk_name: str):
    lsblk = Command(f"lsblk --json {disk_name}")
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
        if partition["size"] == "512M":
            efi_partition = f"/dev/{partition_name}"
        else:
            btrfs_partition = f"/dev/{partition_name}"
    return efi_partition, btrfs_partition

def list_subvolumes(btrfs_partition):
    mount = Command(f"mount {btrfs_partition} /mnt")
    mount.run()

    btrfs = Command(f"btrfs subvolume list -a /mnt")
    btrfs.run()
    output = btrfs.stdout
    
    paths = set()
    lines = output.split("\n")
    for line in lines:
        fields = line.split(" ")
        path = fields[-1]
        if path:
            paths.add(path)

    umount = Command(f"umount /mnt")
    umount.run()

    return sorted(paths)

