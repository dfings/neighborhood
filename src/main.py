#! /usr/bin/env python

from dataclasses import asdict
import json

import click
import flask

from neighborhood import find


def find_json(address: str) -> str:
    return json.dumps([asdict(r) for r in find(address)])


def handle_request(request: flask.Request) -> str:
    return find_json(request.args.get("address", ""))


# pylint: disable=no-value-for-parameter
# ./src/main.py "123 Main St"
@click.command()
@click.argument("address")
def run_cli(address: str) -> None:
    print(find_json(address))


if __name__ == "__main__":
    run_cli()