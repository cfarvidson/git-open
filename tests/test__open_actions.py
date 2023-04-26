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
        result = runner.invoke(cli.cli, ["actions"])
        assert result.exit_code == 0
        assert "Opening GitHub actions..." in result.output
        assert "Opening https://github.com/cfarvidson/git-open/actions" in result.output
