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
    self.__init__() . self.main() is called at the end of self.__init__()
    with attributes self.storage, self.path, self.wikiname, self.conv, self.data
    being set.

    Internal attributes: Subclasses should overwrite these ones.
        pagename: Name used for title of page.
        mtime: Last modified time in epoch format or None.

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
        cachetime: If-Modified-Since value passed from client
        data: Used for POST.
        conv: Converter function. conv(s) returns html converted string.
    """

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

    def __init__(self, storage, path_, wikiname, conv, data=None, cachetime=0):
        """Initialize.

        Args:
            path_: Path object.
            storage: Storage handler object.
            wikiname: String of name of wiki.
            data: When posting data this val is used.
            conv: Function convert md into html.
        """
        self.storage = storage
        self.path = path_
        self.wikiname = wikiname
        self.data = data
        self.conv = conv
        self.cachetime = cachetime

        self.pagename = path_.path
        self.main()
        return

    def main(self):
        """Method to generate content from Path object.

        This method is called at the end of __init__().
        Subclasses must overwrite this method.
        """
        raise NotImplementedError

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

    pagenav = """<form action=".query" method="get">
<a href=".edit.{name}">Edit</a>
<a href=".hist.{name}">History</a>
|
<a href=".list">List</a>
<input type="text" name="q" value="" />
<input type="submit" name="t" value="Go" />
<input type="submit" name="t" value="Search" />
</form>"""

    dirnav = """ <form action=".query" method="get">
<a href=".hist">History</a>
<a href=".edit.style.css">EditStyle</a>
<!-- a href=".xheaders">ExtraHeaders</a -->
<a href=".zip">Zip</a>
|
<input type="text" name="q" value="" />
<input type="submit" name="t" value="Search" />
<input type="submit" name="t" value="Go" />
</form>
"""

    def main(self):
        if self.path.isstyle:
            self.init_as_style()
            return

        if not self.path.base:
            # path.path ends with "/".
            try:
                self.init_as_page("index")
            except exc.PageNameError:
                self.init_as_list()
            return

        try:
            self.init_as_page()
        except exc.PageNameError:
            if self.storage.isdir(self.path.path):
                raise exc.PermanentRedirection(self.path.base + "/")
                return
            else:
                raise exc.SeeOtherRedirection(".edit." + self.path.base)
        return

    def init_as_style(self):
        self.mtime = self.storage.getmtime((self.path.dir, self.path.base),
                                           dtype="style")
        if self.mtime and self.mtime <= self.cachetime:
            raise exc.PageNotModified

        try:
            self.content_raw = self.storage.load((self.path.dir,
                                                  self.path.base),
                                                 dtype="style")
        except exc.PageNotFoundError:
            self.content_raw = ""
        self.type = "text/css; charset=utf-8"
        return

    def init_as_page(self, base=None):
        if not base:
            base = self.path.base

        page_mtime = self.storage.getmtime((self.path.dir, base), dtype=None)
        cache_mtime = self.storage.getmtime((self.path.dir, base),
                                            dtype="cache")

        if page_mtime and page_mtime <= self.cachetime:
            raise exc.PageNotModified
        elif page_mtime and cache_mtime and page_mtime <= cache_mtime:
            # t1 < t2 means t2 is newer than t1
            # larger time means newer
            cache = self.storage.load((self.path.dir, base), dtype="cache")
            assert cache
            self.content_raw = cache

        else:
            # cache is older
            mdstr = self.storage.load((self.path.dir, base), dtype=None)
            self.content = self.conv(mdstr)
            self.navigation = self.pagenav.format(name=base)
            pid = os.fork()
            if pid == 0:
                self.storage.save((self.path.dir, base), str(self),
                                  dtype="cache")
                os._exit(0)

        self.mtime = page_mtime
        return

    def init_as_list(self):
        ls = self.storage.listdir(os.path.join(self.path.path, self.path.base))
        self.content = (
            "<h1>{path}</h1>\n".format(path=self.path.path) +
            "".join(
                """<a href="{name}">{name}</a><br />\n""".format(name=i)
                for i in ["./", "../"] + ls))

        self.navigation = self.dirnav
        self.pagename = "list: " + self.path.path
        return

def get(storage, path_, wikiname, conv, cachetime=0):
    if path_.op == "":
        return DefContent(storage, path_, wikiname, conv, cachetime=cachetime)
    else:
        try:
            op = importlib.import_module("dowwner.op." + path_.op)
        except ImportError:
            raise exc.OperatorError("{}: Invalid operator".format(path_.op))
        try:
            return op.ContentGET(storage, path_, wikiname, conv,
                                 cachetime=cachetime)
        except AttributeError:
            raise exc.OperatorError("{}: Invalid operator".format(path_.op))

def post(storage, path_, wikiname, conv, data):
    """Post data.

    Args:
        data: Data to post. Directly passed from server.
    """
    try:
        op = importlib.import_module("dowwner.op." + path_.op)
    except ImportError:
        raise exc.OperatorError("{}: Invalid operator".format(path_.op))
    try:
        return op.ContentPOST(storage, path_, wikiname, conv, data=data)
    except AttributeError:
        raise exc.OperatorError("{}: Invalid operator".format(path_.op))
