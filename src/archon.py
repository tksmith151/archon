from namespace.all import *

from src.config import *

install_choices = ['all', 'partition', 'format', 'clean', 'mount', 'bootstrap']

def parse_args():
    root_parser = argparse.ArgumentParser(prog="archon")
    root_subparsers = root_parser.add_subparsers(
        title="commands", help="Arch Linux Operations"
    )

    install_parser = root_subparsers.add_parser("install")
    install_parser.add_argument(
        dest="steps",
        default="all",
        type=str,
        choices=install_choices,
        metavar="STEPS",
        nargs="*",
        help="names of steps to run in the install",
    )
    install_parser.set_defaults(command="install")

    args = root_parser.parse_args()

    return args


def main():
    args = parse_args()
    command = args.command
    inputs = InputManager()
    hardware = HardwareManager()
    if command == "install":
        steps = args.steps
        if "all" in steps:
            _ = inputs.install_disk
            _ = inputs.system_password
            _ = inputs.confirm_wipe
            steps = install_choices
        if "partition" in steps:
            partition(inputs.install_disk)
        if "format" in steps:
            format(inputs.install_disk, inputs.system_password)
        if "clean" in steps:
            _ = inputs.confirm_wipe
            clean(inputs.install_disk, inputs.system_password)
        if "mount" in steps:
            mount(inputs.install_disk, inputs.system_password)
        if "bootstrap" in steps:
            bootstrap()


if __name__ == "__main__":
    main()