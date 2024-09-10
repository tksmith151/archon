from namespace.all import *

class HardwareManager:
    @functools.cached_property
    def cpu_info(self) -> Dict[str, str]:
        cpu_info_path = pathlib.Path("/proc/cpuinfo")
        cpu_info: Dict[str, str] = {}
        with cpu_info_path.open() as file:
            for line in file:
                if line := line.strip():
                    key, value = line.split(":", maxsplit=1)
                    cpu_info[key.strip()] = value.strip()
        return cpu_info
    
    @functools.cached_property
    def mem_info(self) -> Dict[str, int]:
        mem_info_path = pathlib.Path("/proc/meminfo")
        mem_info: Dict[str, int] = {}
        with mem_info_path.open() as file:
            for line in file:
                key, value = line.strip().split(':')
                num = value.split()[0]
                mem_info[key] = int(num)
        return mem_info

    @functools.cached_property
    def loaded_modules(self) -> List[str]:
        modules_path = pathlib.Path('/proc/modules')
        loaded_modules: List[str] = []
        with modules_path.open() as file:
            for line in file:
                loaded_module = line.split(maxsplit=1)[0]
                loaded_modules.append(loaded_module)
        return loaded_modules