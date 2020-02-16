import difflib
import os

from pygments import highlight

from pybetter.cli import diff_lexer, term256_formatter


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


__all__ = ["resolve_paths"]


def create_diff(original_source: str, processed_source: str, source_file: str) -> str:
    diff_text = "".join(
        difflib.unified_diff(
            original_source.splitlines(keepends=True),
            processed_source.splitlines(keepends=True),
            fromfile=source_file,
            tofile=source_file,
        )
    )

    return highlight(diff_text, diff_lexer, term256_formatter)


def prettify_time_interval(time_taken: float) -> str:
    if time_taken > 1.0:
        minutes, seconds = int(time_taken / 60), int(time_taken % 60)
        hours, minutes = int(minutes / 60), int(minutes % 60)
    else:
        # Even if it takes less than a second, precise value
        # may still be of interest to us.
        return f"{int(time_taken*1000)} milliseconds"

    result = []

    if hours:
        result.append(f"{hours} hours")

    if minutes:
        result.append(f"{minutes} minutes")

    if seconds:
        result.append(f"{seconds} seconds")

    return " ".join(result)
