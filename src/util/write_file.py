def write_file(location, data):
    with open(location, "w") as fd:
        fd.write(data)