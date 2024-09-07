from namespace.all import *

def parse_args():
    root_parser = argparse.ArgumentParser(prog="calc")
    root_subparsers = root_parser.add_subparsers(
        title="commands", help="Arch Linux Operations"
    )

    install_parser = root_subparsers.add_parser("install")
    install_parser.add_argument(
        dest="step",
        type=str,
        choices=['partition', 'format', 'mount'],
        metavar="STEP",
        help="installation step",
    )
    install_parser.set_defaults(command="install")

    return root_parser.parse_args()


def main():
    args = parse_args()
    command = args.command
    if command == "install":
        step = args.step
        if step == "partition":
            disk = select_disk()
            partition()

    print(args.step)

if __name__ == "__main__":
    main()