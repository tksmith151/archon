from utility import *

subvolume_mounts = {
    "@arch-root": "/mnt",
    "@arch-log": "/mnt/var/log",
}

def create_subvolumes(btrfs_partition, current_subvolumes):
    Command(f"umount /mnt").run()
    Command(f"mount {btrfs_partition} /mnt").run()
    for needed_subvolume in subvolume_mounts.keys():
        if needed_subvolume in current_subvolumes:
            Command(f"btrfs subvolume delete /mnt/{needed_subvolume}").run()
        Command(f"btrfs subvolume create /mnt/{needed_subvolume}").run()
    Command(f"umount /mnt").run()

def mount(efi_partition, btrfs_partition):
    Command("umount /mnt/efi").run()
    for subvolume, mount in subvolume_mounts.items():
        Command(f"umount {mount}").run()
        Command(f"mount --mkdir -o compress=zstd,subvol={subvolume} {btrfs_partition} {mount}").run()
    Command(f"mount --mkdir {efi_partition} /mnt/efi").run()

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
        "git",
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
    Command(f"pacstrap -K /mnt {' '.join(install_packages)}")

def mount_my(btrfs_partition):
    Command(f"mount --mkdir -o compress=zstd,subvol=@my {btrfs_partition} /mnt/.my").run()

def genfstab():
    Command("genfstab -U /mnt >> /mnt/etc/fstab").run()

def unmount_my():
    Command(f"umount /mnt/.my").run()

def main():
    disk = select_disk()
    efi_partition, btrfs_partition = list_partitions(disk)
    current_subvolumes = list_subvolumes(btrfs_partition)
    create_subvolumes(btrfs_partition, current_subvolumes)
    mount(efi_partition, btrfs_partition)
    # pacstrap()
    mount_my(btrfs_partition)
    genfstab()
    unmount_my()


if __name__ == "__main__":
    main()