import os


def resolve_paths(*paths):
    for path in paths:
        if os.path.isfile(path):
            yield os.path.abspath(path)
        elif os.path.isdir(path):
            if path.endswith("__pycache__"):
                continue

            for dirpath, dirnames, filenames in os.walk(path):
                for fn in filenames:
                    yield os.path.abspath(os.path.join(dirpath, fn))
