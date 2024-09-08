from namespace.standard import *

def bootstrap():
    # TODO: Check for mounts
    Command(f"pacstrap -K /mnt base linux linux-firmware",capture=False)
    # Copy fstab
    copy_file("/tmp/fstab", "/mnt/etc/fstab")
    # Needed for wireless cards
    copy_file("/lib/firmware/regulatory.db", "/mnt/lib/firmware/regulatory.db")
    copy_file("/lib/firmware/regulatory.db.p7s", "/mnt/lib/firmware/regulatory.db.p7s")


def main():
    bootstrap()


if __name__ == "__main__":
    main()