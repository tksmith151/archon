from namespace.standard import *

def bootstrap():
    Command(f"pacstrap -K /mnt base").run()


def main():
    bootstrap()

if __name__ == "__main__":
    main()