from namespace.all import *

class InputManager:
    @functools.cached_property
    def install_disk(self):
        disk_file = "/tmp/install_disk"
        if not check_file(disk_file):
            install_disk = select_disk()
            write_file(disk_file, install_disk)
        install_disk = read_file(disk_file)
        print(disk_file)
        return install_disk
    
    @functools.cached_property
    def system_password(self):
        system_password = get_password("system")
        return system_password