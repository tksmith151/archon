from namespace.all import *

class InputManager:
    @functools.cached_property
    def install_disk(self):
        install_disk = select_disk()
        return install_disk
    
    @functools.cached_property
    def system_password(self):
        system_password = get_password("system")
        return system_password