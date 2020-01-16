import difflib
from typing import List

import click
from pyemojify import emojify

from pybetter.improvements import *

IMPROVEMENTS: List[BaseImprovement] = [
    FixNotInConditionOrder(),
    FixMutableDefaultArgs(),
    FixParenthesesInReturn(),
    FixMissingAllAttribute(),
    FixEqualsNone(),
    FixBooleanEqualityChecks(),
]


def process_file(source: str) -> str:
    tree: cst.Module = cst.parse_module(source)
    modified_tree: cst.Module = tree

    for case in IMPROVEMENTS:
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
@click.argument("sources", type=click.File("r+"), nargs=-1)
def main(sources, noop: bool, show_diff: bool):
    if not sources:
        print(emojify("Nothing to do. :sleeping:"))
        return

    for source_file in sources:
        print(f"--> Processing '{source_file.name}'...")

        original_source: str = source_file.read()
        processed_source: str = process_file(original_source)

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
