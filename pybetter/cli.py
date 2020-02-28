"""Command line interface definition."""

import sys
import time
from typing import FrozenSet, Iterable, List, Tuple, Type

import click
import libcst as cst
from pyemojify import emojify

from pybetter.improvements import (
    BaseImprovement,
    FixBooleanEqualityChecks,
    FixEqualsNone,
    FixMissingAllAttribute,
    FixMutableDefaultArgs,
    FixNotInConditionOrder,
    FixParenthesesInReturn,
    FixTrivialFmtStringCreation,
    FixTrivialNestedWiths,
    FixUnhashableList,
)
from pybetter.utils import create_diff, prettify_time_interval, resolve_paths

ALL_IMPROVEMENTS = (
    FixNotInConditionOrder,
    FixMutableDefaultArgs,
    FixParenthesesInReturn,
    FixMissingAllAttribute,
    FixEqualsNone,
    FixBooleanEqualityChecks,
    FixTrivialFmtStringCreation,
    FixTrivialNestedWiths,
    FixUnhashableList,
)

ALL_CODES = frozenset(improvement.CODE for improvement in ALL_IMPROVEMENTS)


def filter_improvements_by_code(code_list: str) -> FrozenSet[str]:
    codes = frozenset(
        code.strip() for code in code_list.split(",")
    ) - {""}

    if not codes:
        return frozenset()

    wrong_codes = ','.join(codes - ALL_CODES)
    if wrong_codes:
        print(emojify(
            f":no_entry_sign: Unknown improvements selected: {wrong_codes}",
        ))
        return frozenset()

    return codes


def process_file(
    source: str, improvements: Iterable[Type[BaseImprovement]],
) -> Tuple[str, List[BaseImprovement]]:
    """
    Apply some improvements to the source file.

    Arguments:
        source: Python source
        improvements: list of improvements to apply

    Returns:
        A tuple of processed code and list of applied improvements.
    """
    modified_tree: cst.Module = cst.parse_module(source)
    improvements_applied = []

    for case_cls in improvements:
        intermediate_tree = modified_tree
        case = case_cls()
        modified_tree = case.improve(intermediate_tree)

        if not modified_tree.deep_equals(intermediate_tree):
            improvements_applied.append(case)

    return modified_tree.code, improvements_applied


@click.command()
@click.option(
    "--noop",
    is_flag=True,
    default=False,
    help="Do not make any changes to the source files.",
)
@click.option(
    "--diff",
    "show_diff",
    is_flag=True,
    default=False,
    help="Show diff-like output of the changes made.",
)
@click.option(
    "--select",
    "selected",
    type=str,
    metavar="CODES",
    help="Apply only improvements with the provided codes.",
)
@click.option(
    "--exclude",
    "excluded",
    type=str,
    metavar="CODES",
    help="Exclude improvements with the provided codes.",
)
@click.argument("paths", type=click.Path(), nargs=-1)
def main(paths, noop: bool, show_diff: bool, selected: str, excluded: str):
    """Make your code better."""
    if not paths:
        print(emojify("Nothing to do. :sleeping:"))
        return

    selected_improvements = list(ALL_IMPROVEMENTS)

    if selected and excluded:
        print(emojify(
            ":no_entry_sign: '--select' and '--exclude' options"
            " are mutually exclusive!",
        ))
        return

    if selected:
        selected_codes = filter_improvements_by_code(selected)

        selected_improvements = [
            improvement
            for improvement in ALL_IMPROVEMENTS
            if improvement.CODE in selected_codes
        ]
    elif excluded:
        excluded_codes = filter_improvements_by_code(excluded)

        selected_improvements = [
            improvement
            for improvement in ALL_IMPROVEMENTS
            if improvement.CODE not in excluded_codes
        ]

    if not selected_improvements:
        print(emojify(":sleeping: No improvements to apply."))
        return

    python_files = filter(lambda fn: fn.endswith(".py"), resolve_paths(*paths))

    total_start_ts = time.process_time()
    for path_to_source in python_files:
        with open(path_to_source, "r+") as source_file:
            original_source: str = source_file.read()

            start_ts = time.process_time()
            processed_source, applied = process_file(
                original_source, selected_improvements,
            )
            end_ts = time.process_time()

            if original_source == processed_source:
                continue

            print(f"--> Fixed '{source_file.name}'...")
            for case in applied:
                print(f"  [+] ({case.CODE}) {case.DESCRIPTION}")
            print()
            print(f"  Time taken: {end_ts - start_ts:.2f} seconds")

            if show_diff:
                print()
                print(
                    create_diff(
                        original_source,
                        processed_source,
                        source_file.name,
                        # ANSI codes used for highlighting source code
                        # will be saved to file and cause `patch` to bail out.
                        highlight=sys.stderr.isatty(),
                    ),
                    file=sys.stderr,
                )

            if noop:
                continue

            source_file.seek(0)
            source_file.truncate()
            source_file.write(processed_source)

            print()

    time_taken = prettify_time_interval(time.process_time() - total_start_ts)
    print(emojify(f":sparkles: All done! :sparkles: :clock2: {time_taken}"))


__all__ = ("main", "process_file")
