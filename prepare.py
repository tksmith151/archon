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
            output.append(device_name)
    if not disks:
        raise Exception("No disks found")
    display_lines(disks)
    return output


def partition():
    efi = Command()
    efi.add("Create efi partition")
    efi.set("")
    efi.show_summary()

    root = Command()
    root.add("Create root partition")
    root.set("")
    root.show_summary()


def main():
    disks = list_disks()
    # partition()

if __name__ == "__main__":
    main()