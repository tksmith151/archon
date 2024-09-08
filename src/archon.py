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
        choices=['partition', 'mount'],
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
        disk = select_disk()
        if "partition" in steps:
            partition(disk)
        if "mount" in steps:
            mount(disk)


if __name__ == "__main__":
    main()