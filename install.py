from utility import *

def pacstrap():
    # This will install some packages to "bootstrap" methaphorically our system. Feel free to add the ones you want
    # "base, linux, linux-firmware" are needed. If you want a more stable kernel, then swap linux with linux-lts
    # "base-devel" base development packages
    # "git" to install the git vcs
    # "btrfs-progs" are user-space utilities for file system management ( needed to harness the potential of btrfs )
    # "grub" the bootloader
    # "efibootmgr" needed to install grub
    # "grub-btrfs" adds btrfs support for the grub bootloader and enables the user to directly boot from snapshots
    # "inotify-tools" used by grub btrfsd deamon to automatically spot new snapshots and update grub entries
    # "timeshift" a GUI app to easily create,plan and restore snapshots using BTRFS capabilities
    # "amd-ucode" microcode updates for the cpu. If you have an intel one use "intel-ucode"
    # "vim" my goto editor, if unfamiliar use nano
    # "networkmanager" to manage Internet connections both wired and wireless ( it also has an applet package network-manager-applet )
    # "pipewire pipewire-alsa pipewire-pulse pipewire-jack" for the new audio framework replacing pulse and jack. 
    # "wireplumber" the pipewire session manager.
    # "reflector" to manage mirrors for pacman
    # "zsh" my favourite shell
    # "zsh-completions" for zsh additional completions
    # "zsh-autosuggestions" very useful, it helps writing commands [ Needs configuration in .zshrc ]
    # "openssh" to use ssh and manage keys
    # "man" for manual pages
    # "sudo" to run commands as other users
    install_packages = [
        "base linux linux-firmware",
        "base-devel",
        "amd-ucode",
        "efibootmgr grub",
        "grub-btrfs btrfs-progs inotify-tools timeshift",
        "networkmanager",
        "pipewire pipewire-alsa pipewire-pulse pipewire-jack wireplumber",
        "reflector",
        "git",
        "openssh",
        "man",
        "sudo",
    ]
    Command(f"pacstrap -K /mnt {' '.join(install_packages)}").run(show_progress=True)


def main():
    pacstrap()
    copy_file("/tmp/fstab", "/mnt/etc/fstab")
    copy_file("/lib/firmware/regulatory.db", "/mnt/lib/firmware/regulatory.db")
    copy_file("/lib/firmware/regulatory.db.p7s", "/mnt/lib/firmware/regulatory.db.p7s")

if __name__ == "__main__":
    main()