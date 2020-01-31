#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function
import webbrowser
import pytest
import sh
from .helpers import python_version_2, python_version_3

if python_version_2():
    from mock import patch
if python_version_3():
    from unittest.mock import patch

from click.testing import CliRunner

from git_open import cli
from git_open.git_open import GitOpen


def test_get_branch_method():
    with patch.object(sh, "git", return_value="MOCKED_BRANCH"):
        branch = GitOpen.get_current_branch()
        assert branch == "MOCKED_BRANCH"


def test_add_commit_to_url__method():
    with patch.object(GitOpen, "get_current_commit_hash", return_value="MOCKED_HASH"):
        git_repo = GitOpen()
        git_repo.add_commit_to_url()
        assert (
            git_repo.url == "https://github.com/cfarvidson/git-open/commit/MOCKED_HASH"
        )


@pytest.mark.parametrize(
    "mocked_return_value,expected",
    [
        (
            "https://github.com/cfarvidson/git-open",
            "Opening https://github.com/cfarvidson/git-open/tree/MOCKED_BRANCH",
        )
    ],
)
def test_command(mocked_return_value, expected):
    mocked_hash_method = patch.object(
        GitOpen, "get_current_branch", return_value="MOCKED_BRANCH"
    )
    mocked_make_url_method = patch.object(
        GitOpen, "make_url", return_value=mocked_return_value
    )
    mocked_open_method = patch.object(webbrowser, "open", return_value=True)
    with mocked_hash_method, mocked_open_method, mocked_make_url_method:
        runner = CliRunner()
        result = runner.invoke(cli.cli, ["branch"])
        assert result.exit_code == 0
        assert "Opening branch..." in result.output
        assert expected in result.output
