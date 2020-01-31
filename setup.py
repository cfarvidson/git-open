#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""The setup script."""
import codecs
import os
import re

from setuptools import setup, find_packages

###############################################################################
NAME = "git-open"
PACKAGES = find_packages(where="src")
META_PATH = os.path.join("src", "git_open", "__init__.py")
KEYWORDS = ["terminal", "git", "web"]
PROJECT_URLS = {
    "Bug Tracker": "https://github.com/cfp2000/git-open/issues",
    "Source Code": "https://github.com/cfp2000/git-open",
}
CLASSIFIERS = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "Natural Language :: English",
    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: Implementation :: CPython",
    "Programming Language :: Python :: Implementation :: PyPy",
    "Topic :: Utilities",
]
INSTALL_REQUIRES = ["Click>=6.7", "sh>=1.12.14", "six>=1.11.0"]
EXTRAS_REQUIRE = {
    "docs": ["sphinx"],
    "setup": ["wheel"],
    "tests": ["pytest", "coverage", "flake8", "six"],
}
EXTRAS_REQUIRE["dev"] = (
    EXTRAS_REQUIRE["tests"] + EXTRAS_REQUIRE["docs"] + ["pre-commit"]
)
ENTRY_POINTS = {"console_scripts": ["git-open=git_open.cli:cli"]}
###############################################################################
HERE = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    """
    Build an absolute path from *parts* and and return the contents of the
    resulting file.  Assume UTF-8 encoding.
    """
    with codecs.open(os.path.join(HERE, *parts), "rb", "utf-8") as f:
        return f.read()


META_FILE = read(META_PATH)


def find_meta(meta):
    """
    Extract __*meta*__ from META_FILE.
    """
    meta_match = re.search(
        r"^__{meta}__ = ['\"]([^'\"]*)['\"]".format(meta=meta), META_FILE, re.M
    )
    if meta_match:
        return meta_match.group(1)

    raise RuntimeError("Unable to find __{meta}__ string.".format(meta=meta))


VERSION = find_meta("version")
URL = find_meta("url")
LONG = read("README.md") + "\n\n" + read("CHANGELOG.md")
if __name__ == "__main__":
    setup(
        name=NAME,
        description=find_meta("description"),
        license=find_meta("license"),
        url=URL,
        project_urls=PROJECT_URLS,
        version=VERSION,
        author=find_meta("author"),
        author_email=find_meta("email"),
        maintainer=find_meta("author"),
        maintainer_email=find_meta("email"),
        keywords=KEYWORDS,
        long_description=LONG,
        long_description_content_type="text/markdown",
        packages=PACKAGES,
        package_dir={"": "src"},
        zip_safe=False,
        include_package_data=True,
        install_requires=INSTALL_REQUIRES,
        classifiers=CLASSIFIERS,
        test_suite="tests",
        extras_require=EXTRAS_REQUIRE,
        entry_points=ENTRY_POINTS,
    )
