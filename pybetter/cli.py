import sys
import time
from typing import List, FrozenSet, Tuple, Type, Iterable

import libcst as cst
import click
from pyemojify import emojify

from pybetter.improvements import (
    FixNotInConditionOrder,
    BaseImprovement,
    FixMutableDefaultArgs,
    FixParenthesesInReturn,
    FixMissingAllAttribute,
    FixEqualsNone,
    FixBooleanEqualityChecks,
    FixTrivialFmtStringCreation,
    FixTrivialNestedWiths,
    FixUnhashableList,
    FixNotIsConditionOrder,
)
from pybetter.utils import resolve_paths, create_diff, prettify_time_interval

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
    FixNotIsConditionOrder,
)


def filter_improvements_by_code(code_list: str) -> FrozenSet[str]:
    all_codes = frozenset([improvement.CODE for improvement in ALL_IMPROVEMENTS])
    codes = frozenset([code.strip() for code in code_list.split(",")]) - {""}

    if not codes:
        return frozenset()

    wrong_codes = codes.difference(all_codes)
    if wrong_codes:
        print(
            emojify(
                f":no_entry_sign: Unknown improvements selected: {','.join(wrong_codes)}"
            )
        )
        return frozenset()

    return codes


def process_file(
    source: str, improvements: Iterable[Type[BaseImprovement]]
) -> Tuple[str, List[BaseImprovement]]:
    tree: cst.Module = cst.parse_module(source)
    modified_tree: cst.Module = tree
    improvements_applied = []

    for case_cls in improvements:
        intermediate_tree = modified_tree
        case = case_cls()
        modified_tree = case.improve(intermediate_tree)

        if not modified_tree.deep_equals(intermediate_tree):
            improvements_applied.append(case)

    return modified_tree.code, improvements_applied


@click.group()
def cli():
    pass


@cli.command()
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
@click.option(
    "--exit-code",
    "exit_code",
    type=int,
    metavar="<CODE>",
    default=0,
    help="Exit with provided code if fixes were applied.",
)
@click.argument("paths", type=click.Path(), nargs=-1)
def main(
    paths, noop: bool, show_diff: bool, selected: str, excluded: str, exit_code: int
):
    if not paths:
        print(emojify("Nothing to do. :sleeping:"))
        return

    selected_improvements = list(ALL_IMPROVEMENTS)

    if selected and excluded:
        print(
            emojify(
                ":no_entry_sign: '--select' and '--exclude' options are mutually exclusive!"
            )
        )
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

    are_fixes_applied = False
    total_start_ts = time.process_time()
    for path_to_source in python_files:
        with open(path_to_source, "r+") as source_file:
            original_source: str = source_file.read()

            start_ts = time.process_time()
            processed_source, applied = process_file(
                original_source, selected_improvements
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

            are_fixes_applied = True

            if noop:
                continue

            source_file.seek(0)
            source_file.truncate()
            source_file.write(processed_source)

            print()

    time_taken = prettify_time_interval(time.process_time() - total_start_ts)
    print(emojify(f":sparkles: All done! :sparkles: :clock2: {time_taken}"))

    if are_fixes_applied:
        sys.exit(exit_code)


__all__ = ["main", "process_file", "ALL_IMPROVEMENTS"]
