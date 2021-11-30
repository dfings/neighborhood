#! /usr/bin/env python

from dataclasses import asdict

import click

from neighborhood import find


# pylint: disable=no-value-for-parameter
# ./src/main.py "123 Main St"
@click.command()
@click.argument("address")
def run_cli(address: str) -> None:
    print([asdict(r) for r in find(address)])


if __name__ == "__main__":
    run_cli()
