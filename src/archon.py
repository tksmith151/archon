from namespace.all import *

def parse_args():
    root_parser = argparse.ArgumentParser(prog="calc")
    root_subparsers = root_parser.add_subparsers(
        title="commands", help="Arch Linux Operations"
    )

    install_parser = root_subparsers.add_parser("install")
    install_parser.add_argument(
        dest="steps",
        type=str,
        choices=['prepare', 'partition', 'mount', 'bootstrap'],
        metavar="STEPS",
        nargs="+",
        help="names of steps to run in the install",
    )
    install_parser.set_defaults(command="install")

    return root_parser.parse_args()


def main():
    args = parse_args()
    command = args.command
    if command == "install":
        steps = args.steps
        disk = None
        if "prepare" in steps:
            prepare()
        if "partition" in steps:
            disk = select_disk(disk)
            partition(disk)
        if "mount" in steps:
            disk = select_disk(disk)
            mount(disk)
        if "bootstrap" in steps:
            bootstrap()


if __name__ == "__main__":
    main()