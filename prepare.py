from utility import *

def list_disks():
    lsblk = Command()
    lsblk.set("lsblk --json")
    lsblk_output = lsblk.run()
    disks: List[str] = []
    for device in json.loads(lsblk_output.stdout).get("blockdevices"):
        device_type = device.get("type")
        if device_type == "disk":
            device_name = device.get("name")
            device_size = device.get("size")
            disks.append(f"{device_name} - {device_size}")
    if not disks:
        raise Exception("No disks found")
    display_lines(disks)


def partition():
    boot = Command()
    boot.add("Create boot partition")
    boot.set("")
    boot.show_summary()

    root = Command()
    root.add("Create root partition")
    root.set("")
    root.show_summary()

    home = Command()
    home.add("Create home partition")
    home.set("")
    home.show_summary()


def main():
    list_disks()
    partition()

if __name__ == "__main__":
    main()