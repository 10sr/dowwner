#!/usr/bin/env python3

# todo: manage history

import os
path = os.path
import urllib

from dowwner.markdown import Markdown

from dowwner.editor import Editor
from dowwner.exc import PageNameError
from dowwner.hist import Hist

class _DirWOLastSlash(BaseException):
    """Dir without last slash."""
    pass

class _Page():
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
        self.path = urllib.parse.unquote(rpath)
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
                raise PageNameError("{}: Invalid page name".format(rpath))

        if elems[-1].startswith(".edit."):
            realrpath = "/".join(elems[:-1] +
                                 [elems[-1].replace(".edit.", "", 1)])
            self.editor = Editor(pages, realrpath)
            self._content = self.editor.content
            self._redirect = None
            return
        elif elems[-1].startswith(".get"):
            qrpath, sep, data = elems[-1].partition("?")
            data = urllib.parse.parse_qs(data)
            self._redirect = ("/".join(elems[:-1]) + "/" +
                              urllib.parse.quote(data["pagename"][0]))
            return
        elif elems[-1].startswith(".rm."):
            realrpath = "/".join(elems[:-1] +
                                 [elems[-1].replace(".rm.", "", 1)])
            self.pages.rm(realrpath)
            self._redirect = "/".join(elems[:-1]) or "/"
            return
        elif elems[-1].startswith(".hist."):
            realrpath = "/".join(elems[:-1] +
                                 [elems[-1].replace(".hist.", "", 1)])
            self.hist = self.pages.hist(realrpath)
            self._content = self.hist.content
            self._redirect = None
            return
        elif elems[-1] == ".list":
            self._content = self.pages.get_dir_content("/".join(elems[:-1]))
            self._redirect = None
            return
        elif elems[-1].startswith("."):
            raise PageNameError("{}: Invalid page name".format(rpath))

        self._redirect = None
        try:
            self._content = self.pages.get_content(self.path)
        except (_DirWOLastSlash, EnvironmentError) as e:
            if isinstance(e, _DirWOLastSlash):
                self._content = None
                self._redirect = rpath + "/"
            elif e.errno == 2:    # No such file or directory
                self._content = None
                self._redirect = "/".join(elems[:-1] + [".edit." + elems[-1]])
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

class _PostPage(_Page):
    def __init__(self, pages, rpath, data):
        self.pages = pages
        self.path = urllib.parse.unquote(rpath)

        elems = rpath.split("/")
        for i in elems[:-1]:
            # if any item other than last one starts with "."
            if i.startswith("."):
                raise PageNameError("Invalid page name: {}".format(rpath))

        assert elems[-1].startswith(".save.")
        realrpath ="/".join(elems[:-1] + [elems[-1].replace(".save.", "", 1)])

        data2 = urllib.parse.parse_qs(data.decode(), keep_blank_values=True)
        content = data2["content"][0]
        self.pages.write_data(realrpath, content)

        self._redirect = realrpath
        return

class Pages():
    FILE_SUFFIX = ".md"

    def __init__(self, rootdir):
        self.dir = rootdir
        self.__md = Markdown()
        self.__hist = Hist(self)
        return

    def get(self, rpath):
        """Return page object for request handler.

        Args:
            path_: Path.
        """
        return _Page(self, rpath)

    def post(self, rpath, data):
        return _PostPage(self, rpath, data)

    def edit(self, rpath):
        """Return editor object for request handler."""
        return Editor(self, rpath)

    def rm(self, rpath):
        """Remove page.

        Returns:
            Path of dirname."""
        self.backup(rpath)
        os.remove(self.gen_fullpath(rpath) + self.FILE_SUFFIX)
        return path.dirname(rpath)

    def hist(self, rpath):
        """Get history file list."""
        return self.__hist.get_list(rpath)

    def backup(self, rpath):
        """Backup rpath."""
        return self.__hist.backup(rpath)

    def write_data(self, rpath, content):
        """Post data.

        Args:
            rpath: relative path to save.
            content: string of content.
        """
        fullpath = self.gen_fullpath(rpath + self.FILE_SUFFIX)
        try:
            os.makedirs(path.dirname(fullpath))
        except OSError as e:
            if e.errno != 17: # 17 means file exists
                raise
        self.backup(rpath)
        with open(fullpath,
                  mode="w", encoding="utf-8") as f:
            f.write(content)
            return True
        return False

    def verify_addr(self, addr):
        return addr == "127.0.0.1"

    def gen_fullpath(self, rpath):
        """Return fullpath from relative path. FILE_SUFFIX is not appended."""
        # note: normpath always strip last "/"
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
            _DirWOLastSlash: dir without last slash.
        """
        fpath = self.gen_fullpath(rpath)

        if path.isdir(fpath):
            if not rpath.endswith("/"):
                raise _DirWOLastSlash()
            ifpath = path.join(fpath, "index")
            irpath = path.join(rpath, "index")
            try:
                return self.__load_file(ifpath, irpath, raw)
            except EnvironmentError as e:
                if e.errno == 2:
                    assert not raw
                    return self.__load_dir(fpath, rpath)
                else:
                    raise
        else:
            return self.__load_file(fpath, rpath, raw)

    def get_dir_content(self, rpath):
        fpath = self.gen_fullpath(rpath)
        return self.__load_dir(fpath, rpath)

    def __load_dir(self, fpath, rpath):
        inputbox = """
<p>
<form action=".get" method="get">
Go or create page: <input type="text" name="pagename" value="" />
</form>
</p>
"""
        items = []
        for l in os.listdir(fpath):
            if l.startswith("."):
                continue
            elif path.isdir(path.join(fpath, l)):
                items.append(l + "/")
            elif l.endswith(self.FILE_SUFFIX):
                items.append(path.splitext(l)[0])

        return ("<h1>{path}</h1>\n".format(path=rpath) +
                "<br />".join("""<a href="{name}">{name}</a>\n""".format(name=i)
                              for i in items) +
                inputbox)

    def __load_file(self, fpath, rpath, raw=False):
        with open(fpath + self.FILE_SUFFIX, encoding="utf-8") as f:
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
<a href=".edit.{name}">Edit</a>
<a href=".hist.{name}">History</a>
<a href=".rm.{name}">Delete</a>
|
<a href=".list">List</a>
</p>
"""
        name = path.basename(rpath)
        conv = self.__md.convert(f.read())
        # rdir = path.dirname(rpath)
        return conv + editlink.format(name=name)
