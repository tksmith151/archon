from namespace.standard import *

def bootstrap():
    # TODO: Check for mounts
    update_pacman()
    update_arch_keyring()
    Command(f"pacstrap -K /mnt {' '.join(bootstrap_packages())}", capture=False)
    # Copy fstab
    copy_file("/tmp/fstab", "/mnt/etc/fstab")
    # Needed for wireless cards
    make_dir("/mnt/usr/lib/firmware/")
    copy_file("/usr/lib/firmware/regulatory.db", "/mnt/usr/lib/firmware/regulatory.db")
    copy_file("/usr/lib/firmware/regulatory.db.p7s", "/mnt/usr/lib/firmware/regulatory.db.p7s")
    # Copy archon to my directory
    base_path = PATH.archon_dir
    Command(f"cp -R {base_path} /mnt/my/archon")




def main():
    bootstrap()


if __name__ == "__main__":
    main()