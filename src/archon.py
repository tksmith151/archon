from namespace.all import *

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
        if "format" in steps:
            disk = select_disk(disk)
            format(disk)
        if "clean" in steps:
            disk = select_disk(disk)
            clean(disk)
        if "mount" in steps:
            disk = select_disk(disk)
            mount(disk)
        if "bootstrap" in steps:
            bootstrap()


if __name__ == "__main__":
    main()