import difflib
import os
from typing import Iterable

from pygments import highlight as highlight_source
from pygments.formatters.terminal256 import Terminal256Formatter
from pygments.lexers.diff import DiffLexer


def resolve_paths(*args: str) -> Iterable(str):
    """Make a flat list of files from list of paths.

    Arguments:
        args: list of file paths

    Yields:
        absolute path to file
    """
    for path in args:
        if os.path.isfile(path):
            yield os.path.abspath(path)
        elif os.path.isdir(path):
            if path.endswith("__pycache__"):
                continue

            for dirpath, _, filenames in os.walk(path):
                for fn in filenames:  # noqa: WPS526
                    yield os.path.abspath(os.path.join(dirpath, fn))


__all__ = ("resolve_paths",)


def create_diff(
    original_source: str,
    processed_source: str,
    source_file: str,
    highlight=False,
) -> str:
    diff_text = "".join(
        difflib.unified_diff(
            original_source.splitlines(keepends=True),
            processed_source.splitlines(keepends=True),
            fromfile=source_file,
            tofile=source_file,
        ),
    )

    if highlight:
        diff_text = highlight_source(
            diff_text, DiffLexer(), Terminal256Formatter(),
        )

    return diff_text


def prettify_time_interval(time_taken: float) -> str:
    if time_taken > 1.0:
        minutes, seconds = int(divmod(time_taken, 60))
        hours, minutes = int(divmod(minutes, 60))
    else:
        # Even if it takes less than a second, precise value
        # may still be of interest to us.
        return f"{int(time_taken*1000)} milliseconds"

    segments = []

    if hours:
        segments.append(f"{hours} hours")

    if minutes:
        segments.append(f"{minutes} minutes")

    if seconds:
        segments.append(f"{seconds} seconds")

    return " ".join(segments)
