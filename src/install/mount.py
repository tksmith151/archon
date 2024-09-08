from namespace.standard import *

subvolume_mounts = {
    "@home": "/mnt/home",
    "@log": "/mnt/var/log",
    "@pkg": "/mnt/var/cache/pacman/pkg",
    "@.snapshots": "/mnt/.snapshots",
}

def mount(disk_name: str):
    print("This action wipe previous arch subvolumes")
    print("and result in the loss of any current arch install")
    confirmed = confirm(really=True)
    if not confirmed:
        return
    
    btrfs_partition = "/dev/mapper/btrfs"
    partitions = get_partitions()

    # Unlock luks if necessary
    if not os.path.exists(btrfs_partition):
        Command(f"cryptsetup open --type luks {partitions['luks']} btrfs").run(show_progress=True)
    
    current_subvolumes = list_subvolumes(btrfs_partition)
    Command(f"umount /mnt").run()
    Command(f"mount {btrfs_partition} /mnt").run()
    for needed_subvolume in subvolume_mounts.keys():
        if needed_subvolume in current_subvolumes:
            Command(f"btrfs subvolume delete /mnt/{needed_subvolume}").run()
        Command(f"btrfs subvolume create /mnt/{needed_subvolume}").run()
    Command(f"umount /mnt").run()

    # Clean mounts
    Command("umount /mnt/efi").run()
    Command("umount /mnt/boot").run()
    Command("umount /mnt/my").run()
    Command("umount /mnt/var/log").run()
    Command("umount /mnt/var/cache/pacman/pkg").run()
    Command("umount /mnt/.snapshots").run()
    Command("umount /mnt").run()

    # Mount btrfs arch subvolumes
    Command(f"mount --mkdir -o compress=zstd,subvol=@ {btrfs_partition} /mnt").run()
    for subvolume, mount in subvolume_mounts.items():
        Command(f"mount --mkdir -o compress=zstd,subvol={subvolume} {btrfs_partition} {mount}").run()

    # Mount boot
    Command(f"mount --mkdir {partitions['boot']} /mnt/boot").run()

    # Mount @my
    Command(f"mount --mkdir -o compress=zstd,subvol=@my {btrfs_partition} /mnt/my").run()

    # Generate fstab
    fstab = Command("genfstab -U /mnt").run().stdout
    write_file("/tmp/fstab", fstab)

    # Mount efi after generating fstab
    Command(f"mount --mkdir {partitions['efi']} /mnt/efi").run()



def main():
    Command("umount -R /mnt")
    disk = select_disk()
    


if __name__ == "__main__":
    main()