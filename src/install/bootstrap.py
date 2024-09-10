from namespace.standard import *

def bootstrap():
    # TODO: Check for mounts
    Command(f"pacstrap -K /mnt {' '.join(base_packages())}", capture=False)
    # Command(f"pacstrap -K /mnt {' '.join(kernel_packages())}", capture=False)
    # Copy fstab
    copy_file("/tmp/fstab", "/mnt/etc/fstab")
    # Needed for wireless cards
    copy_file("/usr/lib/firmware/regulatory.db", "/mnt/usr/lib/firmware/regulatory.db")
    copy_file("/usr/lib/firmware/regulatory.db.p7s", "/mnt/usr/lib/firmware/regulatory.db.p7s")


def main():
    bootstrap()


if __name__ == "__main__":
    main()