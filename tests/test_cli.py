from __future__ import absolute_import

from click.testing import CliRunner
from unittest.mock import patch
from git_open import cli


@patch("webbrowser.open")
def test_open(mock_open_browser):
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert mock_open_browser.called
    mock_open_browser.assert_called_with("https://github.com/cfp2000/git-open")
    assert "Opening https://github.com/cfp2000/git-open" in result.output
