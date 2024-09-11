from namespace.common import *

def base_packages():
    return [
        "base",
        "python",
        # "linux",
        # "linux-firmware",
        # Wireless service
        # "iwd",
    ]

def bootstrap_packages():
    output = base_packages()
    return output

def get_configured_packages():
    base_path = pathlib.Path(__file__).parent.parent.parent.resolve()
    packages_file = base_path / "conf" / "packages"
    text = read_file(str(packages_file))
    lines = text.split("\n")
    packages = bootstrap_packages()
    for line in lines:
        if line[0] == '#':
            continue
        line_packages = line.split(" ")
        packages.extend(line_packages)
    output = list(dict.fromkeys(packages))
    return output

def update_mirrors():
    # reflector command
    # reflector --connection-timeout 1 --threads 2 --url https://archlinux.org/mirrors/status/tier/1/json/ --protocol https --sort rate --country US,CA --save /etc/pacman.d/mirrorlist
    base_path = pathlib.Path(__file__).parent.parent.parent.resolve()
    mirror_list_file = base_path / "conf" / "mirrorlist"
    copy_file(mirror_list_file, "/etc/pacman.d/mirrorlist")

def config_pacman():
    base_path = pathlib.Path(__file__).parent.parent.parent.resolve()
    pacman_conf = base_path / "conf" / "pacman.conf"
    copy_file(pacman_conf, "/etc/pacman.conf")

def update_pacman():
    Command("pacman -Sy --noconfirm", capture=False)

def update_arch_keyring():
    Command("pacman -S --noconfirm archlinux-keyring", capture=False)