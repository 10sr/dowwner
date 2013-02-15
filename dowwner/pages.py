#!/usr/bin/env python3

import os
path = os.path
from io import StringIO

from markdown import Markdown

from dowwner.exc import PageNameError

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
            rpath: Path relative to rootdir.
        """
        self.pages = pages
        self.dir = pages.dir
        self.path = rpath
        self.exists = True
        try:
            self.content = self.pages.get_content(self.path).encode()
        except EnvironmentError as e:
            print(e)
            if e.errno == 2:    # No such file or directory
                self.content = b""
                self.exists = False
            else:
                raise
        return

    # @property
    # def exists(self):
    #     return self.pages.exists(self.path)

    # @property
    # def content(self):
    #     """Return content in bytes."""

class Pages():
    def __init__(self, rootdir):
        self.dir = rootdir
        self.__md = Markdown(extensions=["wikilinks(base_url=,end_url=)"])
        return

    def get(self, rpath):
        """Return page object for request handler.

        Args:
            path_: Path.
        """
        return _Page(self, rpath)

    def post(self, rpath, content):
        """Post data.

        Args:
            rpath: relative path to save.
            content: string of content.
        """
        print(rpath)
        print(content)
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
        fpath = path.normpath(path.join(self.dir, rpath))
        # fpath must be under rootdir for security reason.
        assert fpath.startswith(self.dir)
        return fpath

    def get_content(self, rpath):
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
            print(rpath)
            print(fpath)
            return self.__load_dir(fpath, rpath)

        # if l[-1] == "":
        #     # if rpath ends with "/" or is empty str
        #     try:
        #         print(fpath + "index")
        #         return self.__load_file(fpath + "index")
        #     except EnvironmentError as e:
        #         if e.errno == 2:
        #             return self.__load_dir(fpath, rpath)
        #         else:
        #             raise

        if path.isdir(fpath):
            ifpath = path.join(fpath, "index")
            irpath = path.join(rpath, "index")
            try:
                return self.__load_file(ifpath, irpath)
            except EnvironmentError as e:
                return self.__load_dir(fpath, rpath)
        else:
            return self.__load_file(fpath, rpath)

    def __load_dir(self, fpath, rpath):
        inputbox = """
<p>
<form action="/.get/{path}" method="get">
Go or create page: <input type="text" name="pagename" value="" />
</form>
</p>
"""
        if not rpath.endswith("/") and rpath != "":
            rpath = rpath + "/"

        items = []
        for l in os.listdir(fpath):
            if l.startswith("."):
                continue
            elif path.isdir(path.join(fpath, l)):
                items.append(l + "/")
            elif l.endswith(FILE_SUFFIX):
                items.append(path.splitext(l)[0])

        return ("<h1>dir.</h1>" +
                "<br />".join(items) +
                inputbox.format(path=rpath))

    def __load_file(self, fpath, rpath):
        with open(fpath + FILE_SUFFIX, encoding="utf-8") as f:
            return self.__gen_page(f, rpath)

    def __gen_page(self, f, rpath):
        editlink = """
<p>
<a href="/.edit/{path}">Edit</a>
</p>
"""
        conv = self.__md.convert(f.read())
        return editlink.format(path=rpath) + conv
