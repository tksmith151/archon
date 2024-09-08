from namespace.common import *

def get_partitions(disk_name: str):
    try:
        sfdisk = Command(f"sfdisk --json {disk_name}", quiet=True)
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