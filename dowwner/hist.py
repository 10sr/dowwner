#!/usr/bin/env python3

"""Manage history."""

import os
path = os.path

from dowwner.exc import PageNameError

class _HistList():
    def __init__(self, pages, rpath):
        self.pages = pages
        self.content = self.get_list(rpath)
        return

    def get_list(self, rpath):
        """Get history file list.

        Returns:
            String of history file list.
        """
        fpath = self.pages.gen_fullpath(rpath)
        if path.isdir(rpath):
            raise PageNameError("Directory name: {}".format(rpath))
        dpath, fname = path.split(fpath)

        l = []
        for f in os.listdir(dpath):
            if f.startswith(".hist." + fname):
                l.append(f)

        return "<br />\n".join(l)

class Hist():
    def __init__(self, pages):
        self.pages = pages
        return

    def get_list(self, rpath):
        return _HistList(self.pages, rpath)

    def backup(self, rpath):
        """Backup file.

        This should be called everytime files are modified or deleted.
        Backed up files are like .hist.name.20130216_193548
        """
        return

if __name__ == "__main__":
    pass
