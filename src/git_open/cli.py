# -*- coding: utf-8 -*-
from __future__ import absolute_import
import click
import sys
from .git_open import GitOpen
from . import __version__


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """Open a git repo in the browser from the terminal.

    Running the command without any sub-command will open the main page of the repository.
    """
    if ctx.invoked_subcommand is None:
        git_repo = GitOpen()
        git_repo.open_from_terminal()


@cli.command()
def commit():
    """Open the current commit"""
    git_repo = GitOpen()
    click.echo("Opening commit...")
    git_repo.add_commit_to_url()
    git_repo.open_from_terminal()


@cli.command()
@click.option(
    "-t", "--target", default="master", help="Target branch/commit to compare with"
)
def compare(target):
    """Open a compare view"""
    git_repo = GitOpen()
    click.echo("Opening compare...")
    git_repo.add_compare_to_url(target)
    git_repo.open_from_terminal()


@cli.command()
def branch():
    """Open the current branch"""
    git_repo = GitOpen()
    click.echo("Opening branch...")
    git_repo.add_branch_to_url()
    git_repo.open_from_terminal()


@cli.command()
def version():
    """Show the current git-open version"""
    click.echo("version: {}".format(__version__))
    sys.exit()


if __name__ == "__main__":
    cli(obj={})
