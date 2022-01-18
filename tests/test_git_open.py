#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function
import pytest
import webbrowser

from click.testing import CliRunner

from git_open import cli
from git_open.git_open import GitOpen


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    help_result = runner.invoke(cli.cli, ["--help"])
    assert help_result.exit_code == 0
    assert "Show this message and exit." in help_result.output


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (
            "origin	git@git.myserver.com:username/git_open.git (fetch)\n"
            "origin	git@git.myserver.com:username/git_open.git (push)",
            "origin	git@git.myserver.com:username/git_open.git (fetch)",
        ),
        (
            "origin	git@git.myserver.com:username/git_open.git (fetch)\n"
            "origin	git@git.myserver.com:username/git_open.git (push)",
            "origin	git@git.myserver.com:username/git_open.git (fetch)",
        ),
    ],
)
def test_get_origin_line(test_input, expected):
    remote_string = test_input
    origin_line = GitOpen.get_origin_line(remote_string)
    assert origin_line == expected
    # Test an empty string (no remotes)
    with pytest.raises(SystemExit):
        origin_line = GitOpen.get_origin_line("")
        assert origin_line is None


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (
            "origin	git@git.myserver.com:username/git_open.git (fetch)",
            "git.myserver.com:username/git_open",
        ),
        (
            "origin	git@github.com:username/git_open.git (fetch)",
            "github.com:username/git_open",
        ),
        (
            "origin	https://github.com/username/git_open.git (fetch)",
            "github.com/username/git_open",
        ),
        (
            "origin	https://bitbucket.com/blah/blah/git_open.git (fetch)",
            "bitbucket.com/blah/blah/git_open",
        ),
        (
            "origin	git@bitbucket.com:username/blah/git_open.git (fetch)",
            "bitbucket.com:username/blah/git_open",
        ),
        (
            "origin	git@bitbucket.org:some-namespace/some-repo.git (fetch)",
            "bitbucket.org:some-namespace/some-repo",
        ),
        (
            "origin	https://github.com/qmk/qmk_firmware (fetch)",
            "github.com/qmk/qmk_firmware",
        ),
        (
            "origin	ssh://git@gitlab.some-domain.com:2222/user/some-repo.git (fetch)",
            "gitlab.some-domain.com:2222/user/some-repo",
        ),
        (
            "origin	git+ssh://git@gitlab.some-domain.com:2222/user/some-repo.git (fetch)",
            "gitlab.some-domain.com:2222/user/some-repo",
        ),
    ],
)
def test_filter_origin_line(test_input, expected):
    assert GitOpen.filter_origin_line(test_input) == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (
            "git.myserver.com:username/git_open",
            "https://git.myserver.com/username/git_open",
        ),
        ("github.com:username/git_open", "https://github.com/username/git_open"),
        (
            "bitbucket.org:some-namespace/some-repo",
            "https://bitbucket.org/some-namespace/some-repo",
        ),
        (
            "bitbucket.org/some-namespace/some-repo",
            "https://bitbucket.org/some-namespace/some-repo",
        ),
        (
            "gitlab.some-domain.com:2222/user/some-repo",
            "https://gitlab.some-domain.com:2222/user/some-repo",
        ),
        (
            "github.com/qmk/qmk_firmware",
            "https://github.com/qmk/qmk_firmware",
        ),
    ],
)
def test_make_url(test_input, expected):
    assert GitOpen.make_url(test_input) == expected


@pytest.mark.parametrize("test_input", ["git@bitbucket.org:some-namespace/some-repo"])
def test_make_url_exception(test_input):
    with pytest.raises(NotImplementedError):
        GitOpen.make_url(test_input)
