#!/usr/bin/env python3

# todo: manage history

import os
path = os.path
import urllib

from dowwner.path import Path
from dowwner.file import File
from dowwner import op as dop

class _DirWOLastSlash(BaseException):
    """Dir without last slash."""
    pass

class Pages():
    """Content object for request handler.

    Attributes:
        path: Relative path for content.
        redirect: If need redirect, Location url.
        content: Bytes of content.
    """

    def __init__(self, pages, rpath):
        """
        Args:
            pages: Pages object.
            rpath: Path relative to rootdir. Always starts with "/".
        """
        self.pages = pages
        rpath = urllib.parse.unquote(rpath)
        rpath, getsep, data = rpath.partition("?")
        self.path = rpath
        self._redirect = None

        elems = rpath.split("/")
        # "/" -> ["", ""]
        # "/a" -> ["", "a"]
        # "/.edit.a" -> ["", ".edit.a"]
        # "/dir/" -> ["", "dir", ""]
        # "/dir/.edit.f" -> ["", "dir", ".edit.f"]
        for i in elems[:-1]:
            # if any item other than last one starts with "."
            if i.startswith("."):
                # not work when pagename of get contains slashes
                raise PageNameError("{}: Invalid page name".format(rpath))

        if elems[-1].startswith(".edit."):
            realrpath = "/".join(elems[:-1] +
                                 [elems[-1].replace(".edit.", "", 1)])
            self.editor = Editor(pages, realrpath)
            self._content = self.editor.content
            self._redirect = None
            return
        elif elems[-1].startswith(".revert."):
            dirname, slash, basename = rpath.rpartition("/")
            bakpath = dirname + "/" + basename.replace(".revert", ".bak", 1)
            realrpath = (dirname + "/" + ".".join(basename.split(".")[3:]))
            self.editor = Editor(pages, realrpath,
                                 self.pages.get_raw_content(bakpath))
            self._content = self.editor.content
            self._redirect = None
            return
        elif elems[-1].startswith(".get"):
            # qrpath, sep, data = elems[-1].partition("?")
            data = urllib.parse.parse_qs(data)
            self._redirect = ("/".join(elems[:-1]) + "/" +
                              urllib.parse.quote(data["pagename"][0]))
            return
        elif elems[-1].startswith(".hist."):
            realrpath = "/".join(elems[:-1] +
                                 [elems[-1].replace(".hist.", "", 1)])
            self.hist = self.pages.hist(realrpath)
            self._content = self.hist.content
            self._redirect = None
            return
        elif elems[-1] == ".hist":
            realrpath = "/".join(elems[:-1]) or "/"
            self.hist = self.pages.hist(realrpath)
            self._content = self.hist.content
            self._redirect = None
            return
        elif elems[-1].startswith(".bak."):
            self.hist = self.pages.hist(rpath)
            self._content = self.hist.content
            self._redirect = None
            return
        elif elems[-1] == ".list":
            self._content = self.pages.get_dir_content("/".join(elems[:-1]))
            self._redirect = None
            return
        elif elems[-1].startswith("."):
            raise PageNameError("{}: Invalid page name".format(rpath))
        else:
            self._redirect = None
            try:
                self._content = self.pages.get_content(self.path)
            except (_DirWOLastSlash, EnvironmentError) as e:
                if isinstance(e, _DirWOLastSlash):
                    self._content = None
                    self._redirect = rpath + "/"
                elif e.errno == 2:    # No such file or directory
                    self._content = None
                    self._redirect = "/".join(elems[:-1] +
                                              [".edit." + elems[-1]])
                else:
                    raise
            return

    # todo: use quote for redirect url

    @property
    def redirect(self):
        if self._redirect is None:
            return None
        else:
            return urllib.parse.quote(self._redirect)

    @property
    def content(self):
        if self._content is None:
            return b""
        else:
            return self._content.encode()

class Dowwner():
    """Dowwner main class."""
    def __init__(self, rootdir):
        self.file = File(rootdir)
        return

    def get(self, rpath):
        """Return OP object for request handler.

        Args:
            rpath: Path object.
        """
        p = Path(rpath)
        try:
            return dop.get(self.file, p)
        except KeyError:
            raise PageNameError("Invalid page naem: {}".format(rpath))

    def post(self, rpath, data):
        """Return OP object for request handler.

        Args:
            rpath: Path object.
        """
        p = Path(rpath)
        try:
            return dop.post(self.file, p, data)
        except KeyError:
            raise PageNameError("Invalid page naem: {}".format(rpath))

    def verify_addr(self, addr):
        return addr == "127.0.0.1"
