from namespace.standard import *

def prepare():
    config_pacman()
    update_mirrors()
    update_pacman()
    update_arch_keyring()


def main():
    prepare()


if __name__ == "__main__":
    main()