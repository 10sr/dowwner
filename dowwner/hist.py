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
        self.content = self.gen_list(rpath)
        return

    def gen_list(self, rpath):
        """Get history file list.

        Returns:
            String of history file list.
        """
        fpath = self.pages.gen_fullpath(rpath)
        if path.isdir(fpath):
            dpath = fpath
            fname = ""
        else:
            dpath, fname = path.split(fpath)

        l = []
        neg_suffix_len = len(self.pages.FILE_SUFFIX) * (-1)
        for f in os.listdir(dpath):
            if (f.startswith(".bak.") and
                f.endswith(fname + self.pages.FILE_SUFFIX)):
                l.append(f[:neg_suffix_len])

        l.sort(reverse=True)

        return "<br />\n".join("""<a href="{f}">{f}</a>""".format(f=f)
                               for f in l)

class _BakContent():
    def __init__(self, pages, rpath):
        self.pages = pages
        self.content = self.gen_content(rpath)
        return

    def gen_content(self, rpath):
        return self.pages.get_page_html(rpath)

class Hist():
    def __init__(self, pages):
        self.pages = pages
        return

    def view_file(self, rpath):
        return

    def get(self, rpath):
        elems = rpath.split("/")
        print(rpath)
        if elems[-1].startswith(".bak."):
            return self.get_bak(rpath)
        else:
            return self.get_list(rpath)

    def get_list(self, rpath):
        return _HistList(self.pages, rpath)

    def get_bak(self, rpath):
        return _BakContent(self.pages, rpath)

    def current_time(self):
        return strftime("%Y%m%d_%H%M%S")

    def backup(self, rpath):
        """Backup file.

        This should be called everytime files are modified or deleted.
        Backed up files are like .bak.20130216_193548.name
        """
        # todo: this method should be operated atomic way
        if rpath.endswith("/"):
            raise PageNameError("{}: Cannot backup directory".format(rpath))

        timestr = self.current_time()
        dirname, basename = os.path.split(rpath)
        fulldir = self.pages.gen_fullpath(dirname)
        origpath = os.path.join(fulldir, basename + self.pages.FILE_SUFFIX)
        newpath = os.path.join(fulldir, ".bak." + timestr + "." +
                               basename + self.pages.FILE_SUFFIX)
        try:
            shutil.copyfile(origpath, newpath)
        except EnvironmentError as e:
            if e.errno != 2:
                raise
        return

if __name__ == "__main__":
    pass
