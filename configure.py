from utility import *

def main():
    copy_file("/tmp/fstab", "/mnt/etc/fstab")
    copy_file("/lib/firmware/regulatory.db", "/mnt/lib/firmware/regulatory.db")
    copy_file("/lib/firmware/regulatory.db.p7s", "/mnt/lib/firmware/regulatory.db.p7s")

if __name__ == "__main__":
    main()