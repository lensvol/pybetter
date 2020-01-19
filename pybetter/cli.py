import difflib
from typing import List

import click
from pyemojify import emojify

from pybetter.improvements import *
from pybetter.utils import resolve_paths

ALL_IMPROVEMENTS: List[BaseImprovement] = [
    FixNotInConditionOrder(),
    FixMutableDefaultArgs(),
    FixParenthesesInReturn(),
    FixMissingAllAttribute(),
    FixEqualsNone(),
    FixBooleanEqualityChecks(),
    FixTrivialFmtStringCreation(),
]


def process_file(source: str, improvements: List[BaseImprovement]) -> str:
    tree: cst.Module = cst.parse_module(source)
    modified_tree: cst.Module = tree

    for case in improvements:
        intermediate_tree = modified_tree
        modified_tree = case.improve(intermediate_tree)

        if not modified_tree.deep_equals(intermediate_tree):
            print(f"  [+] ({case.CODE}) {case.DESCRIPTION}")

    return modified_tree.code


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
@click.argument("paths", type=click.Path(), nargs=-1)
def main(paths, noop: bool, show_diff: bool, selected: str):
    if not paths:
        print(emojify("Nothing to do. :sleeping:"))
        return

    python_files = filter(lambda fn: fn.endswith(".py"), resolve_paths(*paths))

    selected_improvements = ALL_IMPROVEMENTS
    if selected:
        all_codes = frozenset([improvement.CODE for improvement in ALL_IMPROVEMENTS])
        selected_codes = frozenset(map(str.strip, selected.split(",")))

        wrong_codes = selected_codes.difference(all_codes)
        if wrong_codes:
            print(
                emojify(
                    f":no_entry_sign: Unknown improvements selected: {','.join(wrong_codes)}"
                )
            )
            return

        selected_improvements = [
            improvement
            for improvement in ALL_IMPROVEMENTS
            if improvement.CODE in selected_codes
        ]

    for path_to_source in python_files:
        with open(path_to_source, "r+") as source_file:
            print(f"--> Processing '{source_file.name}'...")

            original_source: str = source_file.read()
            processed_source: str = process_file(original_source, selected_improvements)

            if original_source == processed_source:
                print("  Nothing changed.")
                continue

            if show_diff:
                print()
                print(
                    "".join(
                        difflib.unified_diff(
                            original_source.splitlines(keepends=True),
                            processed_source.splitlines(keepends=True),
                            fromfile=source_file.name,
                            tofile=source_file.name,
                        )
                    )
                )

            if noop:
                continue

            source_file.seek(0)
            source_file.truncate()
            source_file.write(processed_source)

            print()

    print(emojify(":sparkles: All done! :sparkles:"))
