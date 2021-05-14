# git-open

[![Test](https://github.com/cfarvidson/git-open/workflows/Test/badge.svg?branch=master)](https://github.com/cfarvidson/git-open/actions)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![Maintainability](https://api.codeclimate.com/v1/badges/09be50f0293cfed0e89a/maintainability)](https://codeclimate.com/github/cfp2000/git-open/maintainability)
[![Downloads](http://pepy.tech/badge/git-open)](http://pepy.tech/project/git-open)
[![pypi](https://img.shields.io/pypi/v/git-open.svg)](https://pypi.python.org/pypi/git-open)

Open a git repo in the browser from the terminal.

## Features

From the terminal type the following command to open the current repository in your browser.

### Usage

```
$ git-open --help
Usage: git-open [OPTIONS] COMMAND [ARGS]...

  Open a git repo in the browser from the terminal.

  Running the command without any sub-command will open the main page of the
  repository.

Options:
  --help  Show this message and exit.

Commands:
  branch   Open the current branch
  commit   Open the current commit
  compare  Open a compare view
  version  Show the current git-open version
```

## Installation

### Using pip

    pip install git-open

### Using pipx (recommended)

[pipx](https://github.com/pipxproject/pipx) is a great tool to install python tools globally.

Installing pipx on macOS:

    brew install pipx
    pipx ensurepath

Installing git-open using pipx:

    pipx install git-open

## Credits

This package was initially created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the
[audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage) project template.

## License

GNU General Public License v3.0

See [LICENSE](LICENSE) to see the full text.
