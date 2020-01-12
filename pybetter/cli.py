import click
import libcst as cst

from pybetter.improvements import FixNotInConditionOrder

IMPROVEMENTS = [FixNotInConditionOrder()]


def process_file(source):
    tree = cst.parse_module(source)
    wrapped_tree = cst.MetadataWrapper(tree, unsafe_skip_copy=True)
    modified_tree = wrapped_tree.module

    for case in IMPROVEMENTS:
        intermediate_tree = modified_tree
        modified_tree = case.improve(intermediate_tree)

    return modified_tree.code


@click.group()
def cli():
    pass


@cli.command()
@click.argument("sources", type=click.File("r+"), nargs=-1)
def main(sources):
    for source_file in sources:
        source = source_file.read()
        processed_source = process_file(source)
        source_file.seek(0)
        source_file.truncate()
        source_file.write(processed_source)
