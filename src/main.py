#! /usr/bin/env python

import click

from neighborhood import find


# pylint: disable=no-value-for-parameter
# ./src/main.py "123 Main St"
@click.command()
@click.argument("address")
def run_cli(address: str) -> None:
    print([r.model_dump() for r in find(address)])


if __name__ == "__main__":
    run_cli()
