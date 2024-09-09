from namespace.common import *

def update_mirrors():
    Command("reflector --connection-timeout 1 --sort rate --country US,CA --score 20 --fastest 6 --save /etc/pacman.d/mirrorlist")