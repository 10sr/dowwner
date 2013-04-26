#!/usr/bin/env python3

"""Dowwner classes for operator."""

import sys
import importlib
import urllib
import os

from dowwner import exc
from dowwner import __version__

# todo: provide way to modify header

class BaseContent():
    """Content Base class.

    str(self) and bytes(self) can be used to get contents as html.

    To subclass this method, you should implement self.main(), not overwrite
    self.__init__(). self.main() is called at the end of self.__init__()
    with attributes self.storage, self.path, self.wikiname, self.data being set.

    Attributes:
        redirect: URL encoded path to redirect or None. Relative if not None.

    Internal attributes: Subclasses should overwrite these ones.
        redirect_r: URL unencoded path to redirect or None.
        pagename: Name used for title of page.
        mtime: Last modified time or None.

        content: Html of content of page.
        navigation: Html of navigation menu.
        content_raw: If not None, string of raw content. In this case, content
            and navigation are ignored. Should be used with type != "text/html".
        content_bytes: If not None, bytes of content. In this case, content,
            navigation and content_raw are ignored by __bytes__().

        type: MIME Type of content. Default to "text/html; charset=utf-8".
        filename: Filename. Should be set when type == "application/*"

    Internal readonly attributes:
        path: Path object.
        storage: Storage object.
        data: Used for POST.
    """

    redirect_r = None
    mtime = None

    __html_header = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">"""
    __html_footer = """</html>
"""

    __head_base = """<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<meta name="Generator" content="Dowwner-{version}" />
<!-- <meta http-equiv="Content-Style-Type" content="text/css" />
Not needed when only <link> is used for stylesheets. -->
<link href="common.css" rel="stylesheet" type="text/css" />
<link href="style.css" rel="stylesheet" type="text/css" />
<title>{name}</title>
</head>""".format(version=__version__, name="{name}")

    pagename = ""

    __content_base = """<div id="dowwner-content">
{content}
</div>"""

    content = ""

    __navigation_base = """<div id="dowwner-nav">
{nav}
</div>"""

    navigation = ""

    content_raw = None
    content_bytes = None

    type = "text/html; charset=utf-8"
    filename = None

    def __init__(self, storage, path_, wikiname, data=None):
        """Initialize.

        Args:
            path_: Path object.
            storage: Storage handler object.
            wikiname: String of name of wiki.
            data: When posting data this val is used.
        """
        self.storage = storage
        self.path = path_
        self.wikiname = wikiname
        self.data = data

        self.pagename = path_.path
        self.main()
        return

    def main(self):
        """Method to generate content from Path object.

        This method is called at the end of __init__().
        Subclasses must overwrite this method.
        """
        raise NotImplementedError

    @property
    def redirect(self):
        if self.redirect_r is None:
            return None
        else:
            return urllib.parse.quote(self.redirect_r, encoding="utf-8")

    def __bytes__(self):
        if self.content_bytes is None:
            return str(self).encode("utf-8")
        else:
            return self.content_bytes

    def __str__(self):
        if self.content_raw is None:
            return "\n".join((self.__html_header, self.__head,
                              self.__body, self.__html_footer))
        else:
            return self.content_raw

    @property
    def __head(self):
        return self.__head_base.format(name=self.wikiname +
                                       " :: "
                                       + self.pagename)

    @property
    def __body(self):
        return "\n".join(("<body>",
                          self.__content_base.format(content=self.content),
                          """<hr id="dowwner-sep"/>""",
                          self.__navigation_base.format(nav=self.navigation),
                          "</body>"))

class DefContent(BaseContent):
    """Class used when path has no operator."""

    pagenav = """<p>
<a href=".edit.{name}">Edit</a>
<a href=".hist.{name}">History</a>
|
<a href=".list">List</a>
</p>"""

    dirnav = """ <form action=".go" method="get">
<a href=".hist">History</a>
<a href=".edit.style.css">EditStyle</a>
<a href=".zip">Zip</a>
|
Go <input type="text" name="name" value="" />
</form>"""

    def main(self):
        if self.path.isstyle:
            self.init_as_style()
            return

        if self.path.path.endswith("/"):
            try:
                self.init_as_page("index")
            except exc.PageNameError:
                self.init_as_list()
            return

        try:
            self.init_as_page(self.path.base)
        except exc.PageNameError:
            if self.storage.isdir(self.path):
                self.redirect_r = self.path.base + "/"
                return
            else:
                self.redirect_r = ".edit." + self.path.base
        return

    def init_as_style(self):
        try:
            self.content_raw = self.storage.load(self.path)
        except exc.PageNotFoundError:
            self.content_raw = ""
        else:
            self.mtime = self.storage.getmtime(self.path)
        self.type = "text/css; charset=utf-8"
        return

    def init_as_page(self, name):
        cache = self.storage.load_cache(self.path)

        if cache:
            self.content_raw = cache

        else:
            self.content = self.storage.load(self.path)
            self.navigation = self.pagenav.format(name=name)
            pid = os.fork()
            if pid == 0:
                self.storage.save_cache(self.path, str(self))
                os._exit(0)

        self.mtime = self.storage.getmtime(self.path)
        return

    def init_as_list(self):
        ls = self.storage.listdir(self.path)
        self.content = (
            "<h1>{path}</h1>\n".format(path=self.path.path) +
            "".join(
                """<a href="{name}">{name}</a><br />\n""".format(name=i)
                for i in ["./", "../"] + ls))

        self.navigation = self.dirnav
        self.pagename = "list: " + self.path.path
        return

def get(storage, path_, wikiname):
    if path_.op == "":
        return DefContent(storage, path_, wikiname)
    else:
        try:
            op = importlib.import_module("dowwner.op." + path_.op)
        except ImportError:
            raise exc.OperatorError("{}: Invalid operator".format(path_.op))
        try:
            return op.ContentGET(storage, path_, wikiname)
        except AttributeError:
            raise exc.OperatorError("{}: Invalid operator".format(path_.op))

def post(storage, path_, wikiname, data):
    """Post data.

    Args:
        data: Data to post. Directly passed from server.
    """
    try:
        op = importlib.import_module("dowwner.op." + path_.op)
    except ImportError:
        raise exc.OperatorError("{}: Invalid operator".format(path_.op))
    try:
        return op.ContentPOST(storage, path_, wikiname, data)
    except AttributeError:
        raise exc.OperatorError("{}: Invalid operator".format(path_.op))
