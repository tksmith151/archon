from namespace.common import *

def get_partitions(disk_name: str):
    sfdisk = Command(f"sfdisk --json {disk_name}").run()
    table = json.loads(sfdisk.stdout)["partitiontable"]
    partition_data = table["partitions"]
    partitions: Dict[str, str] = {}
    print(partition_data)
    for partition in partition_data:
        name = partition["name"]
        node = partition["node"]
        partitions[name] = node
    return partitions