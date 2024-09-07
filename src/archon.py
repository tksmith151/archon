import argparse

def parse_args():
    root_parser = argparse.ArgumentParser(prog="calc")
    root_subparsers = root_parser.add_subparsers(
        title="subcommands", help="Arch Linux Operations"
    )

    install_parser = root_subparsers.add_parser("install")
    install_parser.add_argument(
        dest="step",
        type=str,
        choices=['partition', 'format'],
        metavar="STEP",
        help="string indicate the step to run",
    )

    return root_parser.parse_args()


def main():
    args = parse_args()
    print(args.step)

if __name__ == "__main__":
    main()