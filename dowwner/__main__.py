import sys
from typing import List

import click


@click.group()
def cli() -> None:
    # print("main")
    return


@cli.command()
@click.argument("name")
def admin_user(name: str) -> None:
    print("admiN_user {name}")
    return


if __name__ == "__main__":
    cli()
