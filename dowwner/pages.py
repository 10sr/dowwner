#!/usr/bin/env python3

# todo: manage history

import os
path = os.path
from io import StringIO

from dowwner.markdown import Markdown

from dowwner.editor import Editor
from dowwner.exc import PageNameError
from dowwner.hist import Hist

FILE_SUFFIX = ".md"

class _Page():
    """Content object for request handler.

    Attributes:
        path: Relative path for content.
        exists: True if content exists.
        content: Bytes of content.
    """

    def __init__(self, pages, rpath):
        """
        Args:
            pages: Pages object.
            rpath: Path relative to rootdir. Always starts with "/".
        """
        self.pages = pages
        self.dir = pages.dir
        self.path = rpath
        self.exists = True
        try:
            self.content = self.pages.get_content(self.path).encode()
        except EnvironmentError as e:
            if e.errno == 2:    # No such file or directory
                self.content = b""
                self.exists = False
            else:
                raise
        return

class Pages():
    def __init__(self, rootdir):
        self.dir = rootdir
        self.__md = Markdown(extensions=["wikilinks(base_url=,end_url=)"])
        self.__hist = Hist(self)
        return

    def get(self, rpath):
        """Return page object for request handler.

        Args:
            path_: Path.
        """
        return _Page(self, rpath)

    def edit(self, rpath):
        """Return editor object for request handler."""
        return Editor(self, rpath)

    def rm(self, rpath):
        """Remove page.

        Returns:
            Path of dirname."""
        return path.dirname(rpath)

    def hist(self, rpath):
        """Get history file list."""
        return self.__hist.get_list(rpath)

    def post(self, rpath, content):
        """Post data.

        Args:
            rpath: relative path to save.
            content: string of content.
        """
        fullpath = self.gen_fullpath(rpath + FILE_SUFFIX)
        try:
            os.makedirs(path.dirname(fullpath))
        except OSError as e:
            if e.errno != 17: # 17 means file exists
                raise
        with open(fullpath,
                  mode="w", encoding="utf-8") as f:
            f.write(content)
            return True
        return False

    def verify_addr(self, addr):
        return addr == "127.0.0.1"

    def gen_fullpath(self, rpath):
        # normpath always strip last "/"
        fpath = path.normpath(path.join(self.dir, rpath.lstrip("/")))
        # fpath must be under rootdir for security reason.
        assert fpath.startswith(self.dir)
        return fpath

    def get_raw_content(self, rpath):
        return self.get_content(rpath, True)

    def get_content(self, rpath, raw=False):
        """
        Args:
            rpath: Relative path.

        Returns:
            Content string.

        Raises:
            OSError: File not found.
            dowwner.exc.PageNameError: Invalid page name.
        """
        fpath = self.gen_fullpath(rpath)

        l = rpath.split("/")

        for i in l[:-1]:
            # if any item other than last one starts with "."
            if i.startswith("."):
                raise PageNameError("Invalid page name: {}".format(rpath))

        if l[-1] == ".list":
            # if last one is ".list"
            rpath = "/".join(l[:-1])
            fpath = self.gen_fullpath(rpath)
            assert not raw
            return self.__load_dir(fpath, rpath)

        if path.isdir(fpath):
            ifpath = path.join(fpath, "index")
            irpath = path.join(rpath, "index")
            try:
                return self.__load_file(ifpath, irpath, raw)
            except EnvironmentError as e:
                assert not raw
                return self.__load_dir(fpath, rpath)
        else:
            return self.__load_file(fpath, rpath, raw)

    def __load_dir(self, fpath, rpath):
        inputbox = """
<p>
<form action="/.get{path}" method="get">
Go or create page: <input type="text" name="pagename" value="" />
</form>
</p>
"""
        if not rpath.endswith("/"):
            rpath = rpath + "/"

        items = []
        for l in os.listdir(fpath):
            if l.startswith("."):
                continue
            elif path.isdir(path.join(fpath, l)):
                items.append(l + "/")
            elif l.endswith(FILE_SUFFIX):
                items.append(path.splitext(l)[0])

        return ("<h1>{rpath}</h1>\n".format(rpath=rpath) +
                "<br />".join("""<a href="{name}">{name}</a>\n""".format(name=i)
                              for i in items) +
                inputbox.format(path=rpath))

    def __load_file(self, fpath, rpath, raw=False):
        with open(fpath + FILE_SUFFIX, encoding="utf-8") as f:
            if raw:
                return f.read()
            else:
                return self.__gen_page(f, rpath)

    def __gen_page(self, f, rpath):
        # list url not works when viewing dir/index in url like dir.
        # i wonder if it should be fixed.
        # always redirect accessing dir to dir/?
        editlink = """
<hr />
<p>
<a href="/.edit{path}">Edit</a>
<a href="/.hist{path}">History</a>
<a href="/.rm{path}">Delete</a>
|
<a href=".list">List</a>
</p>
"""
        conv = self.__md.convert(f.read())
        # rdir = path.dirname(rpath)
        return conv + editlink.format(path=rpath)
