from namespace.common import *

def get_cpu_vendor():
    lscpu = Command("lscpu --json", capture=True).stdout
    entries = lscpu["lscpu"]
    for entry in entries:
        field = entry.get("field", "")
        if "Vendor ID" in field:
            data = entry.get("data", "")
            if "Intel" in data:
                return "Intel"
            if "AMD" in data:
                return "AMD"
            raise Exception("CPU type not found")
    