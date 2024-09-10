from namespace.all import *

from src.config import *

def parse_args():
    root_parser = argparse.ArgumentParser(prog="calc")
    root_subparsers = root_parser.add_subparsers(
        title="commands", help="Arch Linux Operations"
    )

    install_choices = ['all', 'prepare', 'partition', 'format', 'clean', 'mount', 'bootstrap']
    install_parser = root_subparsers.add_parser("install")
    install_parser.add_argument(
        dest="steps",
        type=str,
        choices=install_choices,
        metavar="STEPS",
        nargs="+",
        help="names of steps to run in the install",
    )
    install_parser.set_defaults(command="install")

    args = root_parser.parse_args()

    if args.command == "install":
        if "all" in args.steps:
            args.steps = install_choices

    return args


def main():
    hardware = HardwareManager
    args = parse_args()
    command = args.command
    inputs = InputManager()
    hardware = HardwareManager()
    if command == "install":
        steps = args.steps
        disk = None
        if "prepare" in steps:
            prepare()
        if "partition" in steps:
            partition(inputs.install_disk)
        if "format" in steps:
            format(inputs.install_disk, inputs.system_password)
        if "clean" in steps:
            clean(inputs.install_disk, inputs.system_password)
        if "mount" in steps:
            mount(inputs.install_disk, inputs.system_password)
        if "bootstrap" in steps:
            bootstrap()


if __name__ == "__main__":
    main()