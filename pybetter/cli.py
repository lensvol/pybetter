from typing import List

import click
from pyemojify import emojify

from pybetter.improvements import *

IMPROVEMENTS: List[BaseImprovement] = [
    FixNotInConditionOrder(),
    FixMutableDefaultArgs(),
    FixParenthesesInReturn(),
]


def process_file(source: str) -> str:
    tree: cst.Module = cst.parse_module(source)
    wrapped_tree: cst.MetadataWrapper = cst.MetadataWrapper(tree, unsafe_skip_copy=True)
    modified_tree: cst.Module = wrapped_tree.module

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
@click.argument("sources", type=click.File("r+"), nargs=-1)
def main(sources, noop: bool):
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

        if noop:
            continue

        source_file.seek(0)
        source_file.truncate()
        source_file.write(processed_source)

        print()

    print(emojify(":sparkles: All done! :sparkles:"))
