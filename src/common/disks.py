from namespace.common import *

def list_disks():
    lsblk = Command("lsblk --json")
    lsblk.run(capture_output=True)
    output: List[Tuple[str, str]] = []
    devices: List[Dict] = json.loads(lsblk.stdout).get("blockdevices")
    for device in devices:
        device_type = device.get("type")
        if device_type == "disk":
            device_name = device.get("name")
            device_size = device.get("size")
            output.append((f"/dev/{device_name}", str(device_size)))
    if not output:
        raise Exception("No disks found")
    return output

def select_disk(disk=None):
    if disk is not None:
        return disk
    output = None
    while output is None:
        disks = list_disks()
        print("Disks:")
        for index, disk in enumerate(disks):
            print(index, disk[0], disk[1])
        try:
            disk_index = int(input("Select disk by index: "))
            disk = disks[disk_index]
            output = disk[0]
        except:
            print("Invalid disk index")
        print()
    return output