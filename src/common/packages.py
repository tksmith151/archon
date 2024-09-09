from namespace.common import *

def get_configured_packages():
    base_path = pathlib.Path(__file__).parent.parent.parent.resolve()
    packages_file = base_path / "conf" / "packages"
    text = read_file(str(packages_file))
    lines = text.split("\n")
    packages = []
    for line in lines:
        if line[0] == '#':
            continue
        line_packages = line.split(" ")
        packages.extend(line_packages)
    output = list(dict.fromkeys(packages))
    return output

def update_mirrors():
    Command("reflector --connection-timeout 1 --threads 2  --protocol https --sort rate --country US,CA --score 20 --save /etc/pacman.d/mirrorlist")

def config_pacman():
    lines = [
        "# See the pacman.conf(5) manpage for option and repository directives \n",
        "[options]",
        "RootDir           = /",
        "DBPath            = /var/lib/pacman/",
        "LogFile           = /var/log/pacman.log",
        "GPGDir            = /etc/pacman.d/gnupg/",
        "HoldPkg           = pacman glibc",
        "SyncFirst         = pacman",
        "XferCommand       = /usr/bin/curl -C - -f %u > %o",
        "CleanMethod       = KeepInstalled",
        "Architecture      = auto",
        "ParallelDownloads = 6",
        "SigLevel = Required DatabaseOptional TrustedOnly",
        "Color",
        "CheckSpace",
        "ILoveCandy"
        "",
        "[core]",
        "SigLevel = PackageRequired",
        "Include = /etc/pacman.d/mirrorlist",
        "",
        "[extra]",
        "SigLevel = PackageRequired",
        "Include = /etc/pacman.d/mirrorlist",
        "",
        "[community]",
        "SigLevel = PackageRequired",
        "Include = /etc/pacman.d/mirrorlist",
        "",
        "[multilib]",
        "SigLevel = PackageRequired",
        "Include = /etc/pacman.d/mirrorlist",
        "",
    ]
    write_file("/etc/pacman.conf", "\n".join(lines))