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

    def __init__(self):
        self.url = ""
        self.remotes = self.get_remotes()
        # Filter the origin line
        origin_line = self.get_origin_line(self.remotes)
        origin_line = self.filter_origin_line(origin_line)
        self.url = self.make_url(origin_line)

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
        origin_line = re.sub("\.git.*$", "", origin_line)
        origin_line = re.sub("\(.*\)", "", origin_line)
        origin_line = origin_line.strip(string.whitespace)
        return origin_line

    @staticmethod
    def make_url(filtered_origin_string):
        """make a url from the filtered string

        'github.com:username/git_open.git' ->
        https://github.com/username/git_open
        """
        if filtered_origin_string.startswith("http"):
            return filtered_origin_string

        elif filtered_origin_string.startswith("git@"):
            filtered_origin_string = filtered_origin_string.replace(":", "/")
            url = filtered_origin_string.replace("git@", "https://")
            return url

        else:
            raise NotImplementedError(
                "The filtered origin string did not start as expected",
                filtered_origin_string,
            )

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
