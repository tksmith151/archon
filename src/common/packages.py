from namespace.common import *

def get_configured_packages():
    base_path = pathlib.Path(__file__).parent.parent.parent.resolve()
    packages_file = base_path / "conf" / "packages"
    lines = read_file(str(packages_file))
    packages = set()
    for line in lines:
        if line[0] == '#':
            continue
        line_packages = set(line.split(" "))
        packages.update(line_packages)
    return packages