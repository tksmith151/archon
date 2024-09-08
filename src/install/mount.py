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
    partitions = get_partitions(disk_name)

    # Unlock luks if necessary
    if not os.path.exists(btrfs_partition):
        Command(f"cryptsetup open --type luks {partitions['luks']} btrfs").run()
    
    current_subvolumes = list_subvolumes(btrfs_partition)
    unmount_all()
    Command(f"mount {btrfs_partition} /mnt").run()
    if "@my" not in current_subvolumes:
        Command("btrfs subvolume create /mnt/@my").run()
    if "@" in current_subvolumes:
        Command(f"btrfs subvolume delete /mnt/@").run()
    Command(f"btrfs subvolume create /mnt/@").run()
    for needed_subvolume in subvolume_mounts.keys():
        if needed_subvolume in current_subvolumes:
            Command(f"btrfs subvolume delete /mnt/{needed_subvolume}").run()
        Command(f"btrfs subvolume create /mnt/{needed_subvolume}").run()

    # Clean mounts
    unmount_all()

    # Mount btrfs arch subvolumes
    Command(f"mount -o compress=zstd,subvol=@ {btrfs_partition} /mnt").run()
    for subvolume, mount in subvolume_mounts.items():
        os.makedirs(mount, exist_ok=True)
        Command(f"mount -o compress=zstd,subvol={subvolume} {btrfs_partition} {mount}").run()

    # Mount boot
    os.makedirs("/mnt/boot", exist_ok=True)
    Command(f"mount {partitions['boot']} /mnt/boot").run()

    # Mount @my
    os.makedirs("/mnt/my", exist_ok=True)
    Command(f"mount -o compress=zstd,subvol=@my {btrfs_partition} /mnt/my").run()

    # Generate fstab
    fstab = Command("genfstab -U /mnt").run(capture_output=True).stdout
    write_file("/tmp/fstab", fstab)

    # Mount efi after generating fstab
    os.makedirs("/mnt/efi", exist_ok=True)
    Command(f"mount {partitions['efi']} /mnt/efi").run()



def main():
    disk = select_disk()
    mount(disk)
    


if __name__ == "__main__":
    main()