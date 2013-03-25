#!/usr/bin/env python3

"""Dowwner classes for operator.

All classes must inherit OP.
"""

import sys
import importlib
import urllib

class OP():
    """OP Base class.

    str(op) and bytes(op) can be used to get contents as html.

    Attributes:
        redirect: URL encoded path to redirect or None. Relative if not None.

    Internal attributes: Subclasses should overwrite these ones
        redirect_r: URL unencoded path to redirect or None.
        pagename: Name used for title of page.
        content: Content of page.
        navigation: Navigation menu.
    """

    redirect_r = None

    __html_header = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">"""
    __html_footer = """</html>
<!-- Page generated by [Dowwner](https://github.com/10sr/dowwner) -->"""

    __head_base = """<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<title>{name}</title>
</head>"""

    pagename = ""

    __content_base = """<div id="dowwner-content">
{content}
</div>"""

    content = ""

    __navigation_base = """<div id="dowwner-nav">
{nav}
</div>"""

    navigation = ""

    def __init__(self, file, path_):
        """Initialize.

        Args:
            path_: Path object.
            file: File handler object.
        """
        self.path = path_
        self.file = file
        self.pagename = path_.path
        return

    @property
    def redirect(self):
        if self.redirect_r is None:
            return None
        else:
            return urllib.parse.quote(self.redirect_r, encoding="utf-8")

    def __bytes__(self):
        return str(self).encode("utf-8")

    def __str__(self):
        return "\n".join((self.__html_header, self.__head,
                          self.__body, self.__html_footer))

    @property
    def __head(self):
        return self.__head_base.format(name=self.pagename)

    @property
    def __body(self):
        return "\n".join(("<body>",
                          self.__content_base.format(content=self.content),
                          """<hr id="dowwner-sep"/>""",
                          self.__navigation_base.format(nav=self.navigation),
                          "</body>"))

class NO_OP(OP):
    """Class used when path has no operator."""

    pagenav = """<p>
<a href=".edit.{name}">Edit</a>
<a href=".hist.{name}">History</a>
|
<a href=".list">List</a>
</p>"""

    dirnav = """<p>
<form action=".go" method="get">
<a href=".hist">History</a>
|
Go <input type="text" name="name" value="" />
</form>
</p>"""

    def __init__(self, file, path_):
        OP.__init__(self, file, path_)

        if file.isdir(path_):
            if not path_.path.endswith("/"):
                self.redirect_r = path_.base + "/"
                return
            try:
                self.init_as_page("index")
            except EnvironmentError as e:
                if e.errno != 2:
                    raise
                self.init_as_list()
        else:
            try:
                self.init_as_page(path_.base)
            except EnvironmentError as e:
                if e.errno == 2:
                    self.redirect_r = ".edit." + path_.base
                    return
                else:
                    raise
        return

    def init_as_page(self, name):
        self.content = self.file.load(self.path)
        self.navigation = self.pagenav.format(name=name)
        return

    def init_as_list(self):
        ls = self.file.listdir(self.path)
        self.content = (
            "<h1>{path}</h1>\n".format(path=self.path.path) +
            "".join(
                """<a href="{name}">{name}</a><br />\n""".format(name=i)
                for i in ls))

        self.navigation = self.dirnav
        self.pagename = "list: " + self.path.path
        return

def get(file, path_):
    if path_.op == "":
        return NO_OP(file, path_)
    else:
        try:
            op = importlib.import_module("dowwner.op." + path_.op)
        except ImportError:
            raise
        try:
            return op.OP_GET(file, path_)
        except AttributeError:
            raise

def post(file, path_, data):
    """Post data.

    Args:
        data: Data to post. Directly passed from server.
    """
    try:
        op = importlib.import_module("dowwner.op." + path_.op)
    except ImportError:
        raise
    try:
        return op.OP_POST(file, path_, data)
    except AttributeError:
        raise
