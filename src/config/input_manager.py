from namespace.all import *

class InputManager:
    @functools.cached_property
    def install_disk(self):
        disk_file = "/tmp/install_disk"
        if not check_file(disk_file):
            install_disk = select_disk()
            write_file(disk_file, install_disk)
        install_disk = read_file(disk_file)
        print(install_disk)
        return install_disk
    
    @functools.cached_property
    def system_password(self):
        password_file = "/tmp/system_password"
        if not check_file(password_file):
            system_password = get_password("system")
            write_file(password_file, system_password)
        system_password = read_file(password_file)
        print(system_password)
        return system_password