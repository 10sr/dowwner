#!/usr/bin/env python3

"""Manage history."""

import os
path = os.path
import shutil
from time import strftime

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
            if f.startswith(".bak." + fname):
                l.append(f)

        return "<br />\n".join(l)

class Hist():
    def __init__(self, pages):
        self.pages = pages
        return

    def view_file(self, rpath):
        return

    def get_list(self, rpath):
        return _HistList(self.pages, rpath)

    def current_time(self):
        return strftime("%Y%m%d_%H%M%S")

    def backup(self, rpath):
        """Backup file.

        This should be called everytime files are modified or deleted.
        Backed up files are like .bak.name.20130216_193548
        """
        # todo: this method should be operated atomic way
        if rpath.endswith("/"):
            raise PageNameError("{}: Cannot backup directory".format(rpath))

        timestr = self.current_time()
        dirname, basename = os.path.split(rpath)
        fulldir = self.pages.gen_fullpath(dirname)
        origpath = os.path.join(fulldir, basename + self.pages.FILE_SUFFIX)
        newpath = os.path.join(fulldir, ".bak." + basename + "." + timestr)
        try:
            shutil.copyfile(origpath, newpath)
        except EnvironmentError as e:
            if e.errno != 2:
                raise
        return

if __name__ == "__main__":
    pass
