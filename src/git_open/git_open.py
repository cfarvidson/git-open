# -*- coding: utf-8 -*-
import re
import string
import sys
import webbrowser
import six
import sh


class GitOpen(object):
    """The class that will open the url to the remote repository from
    terminal"""

    GITLAB = "GITLAB"
    GITHUB = "GITHUB"
    BITBUCKET = "BITBUCKET"

    def __init__(self):
        self.url = ""
        self.remotes = self.get_remotes()
        # Filter the origin line
        origin_line = self.get_origin_line(self.remotes)
        origin_line = self.filter_origin_line(origin_line)
        self.url = self.make_url(origin_line)
        if "github.com" in self.url:
            self.type = GitOpen.GITHUB
        elif "gitlab.com" in self.url:
            self.type = GitOpen.GITLAB
        elif "bitbucket.org" in self.url:
            self.type = GitOpen.BITBUCKET
        else:
            # Default to gitlab since there are many self hosted gitlab servers
            self.type = GitOpen.GITLAB

    @staticmethod
    def get_origin_line(remotes_string):
        """Filter the remote lines and get the first origin one"""
        remotes_list = remotes_string.split("\n")
        # Filter on origin
        origin_remotes_list = [r for r in remotes_list if "origin" in r]
        if origin_remotes_list:
            return origin_remotes_list[0]

        else:
            print("There does not seem to be any remotes.")
            sys.exit(1)

    @staticmethod
    def filter_origin_line(origin_line):
        """Filter the origin line

        'origin	git@github.com:username/git_open.git (fetch)' ->
        github.com:username/git_open.git
        """
        origin_line = re.sub("^origin", "", origin_line)

        # Remove protocols
        origin_line = re.sub("[A-Za-z0-9][A-Za-z0-9+.-]*://", "", origin_line)
        origin_line = re.sub("[A-Za-z0-9][A-Za-z0-9+.-]*@", "", origin_line)

        origin_line = re.sub("\.git.*$", "", origin_line)
        origin_line = re.sub("\(.*\)", "", origin_line)
        origin_line = origin_line.strip(string.whitespace)
        return origin_line

    @staticmethod
    def _handle_ports_in_url(origin_string):
        """Converts : to / if the : is followed by a character

        git@gitlab.some-domain.com:2222/user/some-repo => Does nothing
        git@gitlab.some-domain.com:user/some-repo => git@gitlab.some-domain.com/user/some-repo
        """
        if ":" in origin_string:
            first_char = origin_string.split(":")[1][0]
            try:
                int(first_char)
            except ValueError:
                return origin_string.replace(":", "/")

        return origin_string

    @staticmethod
    def make_url(filtered_origin_string):
        """make a url from the filtered string

        'github.com:username/git_open.git' ->
        https://github.com/username/git_open
        """
        if filtered_origin_string.startswith("git@"):
            raise NotImplementedError(
                "The filtered origin string did not start as expected",
                filtered_origin_string,
            )

        return "https://" + GitOpen._handle_ports_in_url(filtered_origin_string)

    def add_commit_to_url(self):
        current_commit_hash = GitOpen.get_current_commit_hash()
        self.url += "/commit/%s" % current_commit_hash

    def add_compare_to_url(self, target):
        current_commit_hash = GitOpen.get_current_commit_hash()
        prefix = ""
        if self.type == GitOpen.GITLAB:
            prefix = "/-"
        self.url += "%s/compare/%s...%s" % (prefix, target, current_commit_hash)

    def add_branch_to_url(self):
        branch = GitOpen.get_current_branch()
        self.url += "/tree/%s" % branch

    @staticmethod
    def get_remotes():
        try:
            remotes = sh.git("remote", "-v").stdout
            if isinstance(remotes, six.binary_type):
                remotes = remotes.decode()
            return remotes

        except Exception:
            print("Something went wrong.. Is this a git repo?")
            sys.exit(1)

    def open_from_terminal(self):
        """Open the URL via the terminal open command"""
        if self.url:
            print("Opening {}".format(self.url))
            webbrowser.open(self.url)
        else:
            print("Cannot open URL")

    @staticmethod
    def get_current_commit_hash():
        return sh.git("rev-parse", "HEAD").strip()

    @staticmethod
    def get_current_branch():
        return sh.git("rev-parse", "--abbrev-ref", "HEAD").strip()
