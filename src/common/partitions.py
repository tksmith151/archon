from namespace.common import *

def get_partitions(disk_name: str):
    try:
        sfdisk = Command(f"sfdisk --json {disk_name}", quiet=True, supress=True)
        table = json.loads(sfdisk.stdout)["partitiontable"]
        partition_data: List[Dict] = table["partitions"]
        partitions: Dict[str, str] = {}
        for partition in partition_data:
            name = partition.get("name", None)
            if name is None:
                continue
            node = partition["node"]
            partitions[name] = node
        return partitions
    except:
        return None
    
def get_filesystem_type(partition_name: str):
    lsblk = Command(f"lsblk --json {partition_name}", quiet=True)
    devices: List[Dict] = json.loads(lsblk.stdout).get("blockdevices")
    filesystem = devices[0]
    fstype = filesystem["fstype"]
    return fstype
    
def verify_partitions(disk_name: str):
    sfdisk = Command(f"sfdisk --json {disk_name}", quiet=True, supress=True)
    table = json.loads(sfdisk.stdout)["partitiontable"]
    partition_data: List[Dict] = table["partitions"]
    efi_confirmed = False
    boot_confirmed = False
    luks_confirmed = False
    for partition in partition_data:
        name = partition.get("name", None)
        if name is None:
            continue
        node = partition["node"]
        ptype = partition["type"]
        if name == "efi":
            if node[-1] != "1":
                raise Exception("efi partition has wrong number")
            if  ptype != "C12A7328-F81F-11D2-BA4B-00A0C93EC93B":
                raise Exception("efi partition has wrong type")
            efi_confirmed = True

        if name == "boot":
            if node[-1] != "2":
                raise Exception("boot partition has wrong number")
            if ptype != "21686148-6449-6E6F-744E-656564454649":
                raise Exception("boot partition has wrong type")
            boot_confirmed = True

        if name == "luks":
            if node[-1] != "3":
                raise Exception("boot partition has wrong number")
            if ptype != "0FC63DAF-8483-4772-8E79-3D69D8477DE4":
                raise Exception("boot partition has wrong type")
            luks_confirmed = True

    if not efi_confirmed:
        raise Exception("efi partition is missing")
    if not boot_confirmed:
        raise Exception("boot partition is missing")
    if not luks_confirmed:
        raise Exception("luks partition is missing")

    return True