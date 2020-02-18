import difflib
import os

from pygments import highlight as highlight_source

from pygments.formatters.terminal256 import Terminal256Formatter
from pygments.lexers.diff import DiffLexer


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


def create_diff(
    original_source: str, processed_source: str, source_file: str, highlight=False
) -> str:
    diff_text = "".join(
        difflib.unified_diff(
            original_source.splitlines(keepends=True),
            processed_source.splitlines(keepends=True),
            fromfile=source_file,
            tofile=source_file,
        )
    )

    if highlight:
        diff_text = highlight_source(diff_text, DiffLexer(), Terminal256Formatter())

    return diff_text


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
