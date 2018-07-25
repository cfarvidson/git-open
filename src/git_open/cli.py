# -*- coding: utf-8 -*-
from __future__ import absolute_import
import click
import sys
from .git_open import GitOpen
from . import __version__


@click.command()
@click.option("--version", is_flag=True, help="Show the current git-open version")
def main(version):
    """Console script for git_open.

    This script will open a remote repo from the terminal.
    """
    if version:
        print_version()
    git_repo = GitOpen()
    git_repo.open_from_terminal()


def print_version():
    click.echo("version: {}".format(__version__))
    sys.exit()


if __name__ == "__main__":
    main()
