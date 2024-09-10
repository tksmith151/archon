from namespace.all import *

class ConfigManager:
    @functools.cached_property
    def install_disk(self):
        install_disk = select_disk()
        return install_disk
    
    @functools.cached_property
    def root_password(self):
        root_password = get_password("root/luks")
        return root_password
    
    @functools.cached_property
    def username(self):
        username = get_input("username")
        return username

    @functools.cached_property
    def user_password(self):
        user_password = get_password("user")
        return user_password