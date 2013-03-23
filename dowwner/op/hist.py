#!/usr/bin/env python3

"""Manage history."""

import os
path = os.path
import shutil
from time import strftime

from dowwner.exc import PageNameError

import dowwner.op

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
    footer = """
<hr />
<p>
<a href="{name}">Current</a>
<a href="{revert}">Revert</a>
|
<a href=".list">List</a>
</p>
"""

    def __init__(self, pages, rpath):
        self.pages = pages
        self.content = self.gen_content(rpath)
        return

    def gen_content(self, rpath):
        basename = rpath.rpartition("/")[2]
        revert = ".revert." + ".".join(basename.split(".")[2:])
        pagename = rpath.rpartition(".")[2]
        return (self.pages.get_page_html(rpath) +
                self.footer.format(name=pagename, revert=revert))

class OP_GET(dowwner.op.OP):
    def __init__(self, file, path_):
        dowwner.op.OP.__init__(self, file, path_)
        ls = file.lshist(path_)
        c = ("<h1>{path}</h1>\n".format(path=path_.path) +
             "".join("""<a href="{name}">{name}</a><br />\n""".format(name=i)
                     for i in ls) +
             self.dirfooter)

        self.body = "\n".join(("<body>", c, "</body>"))
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

if __name__ == "__main__":
    pass
