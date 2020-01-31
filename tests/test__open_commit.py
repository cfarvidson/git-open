#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function
import webbrowser
from .helpers import python_version_2, python_version_3

if python_version_2():
    from mock import patch
if python_version_3():
    from unittest.mock import patch

from click.testing import CliRunner

from git_open import cli
from git_open.git_open import GitOpen


def test_get_hash__method():
    hash = GitOpen().get_current_commit_hash()
    assert len(hash) == 40


def test_add_commit_to_url__method():
    with patch.object(GitOpen, "get_current_commit_hash", return_value="MOCKED_HASH"):
        git_repo = GitOpen()
        git_repo.add_commit_to_url()
        assert (
            git_repo.url == "https://github.com/cfarvidson/git-open/commit/MOCKED_HASH"
        )


def test_command():
    mocked_hash_method = patch.object(
        GitOpen, "get_current_commit_hash", return_value="MOCKED_HASH"
    )
    mocked_make_url_method = patch.object(
        GitOpen, "make_url", return_value="https://github.com/cfarvidson/git-open"
    )
    mocked_open_method = patch.object(webbrowser, "open", return_value=True)
    with mocked_hash_method, mocked_open_method, mocked_make_url_method:
        runner = CliRunner()
        result = runner.invoke(cli.cli, ["commit"])
        assert result.exit_code == 0
        assert "Opening commit..." in result.output
        assert (
            "Opening https://github.com/cfarvidson/git-open/commit/MOCKED_HASH"
            in result.output
        )
