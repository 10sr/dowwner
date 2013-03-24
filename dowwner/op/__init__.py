#!/usr/bin/env python3

"""Dowwner classes for operator.

All classes must inherit OP.
"""

import sys
import importlib
import urllib

class OP():
    """OP

    Attributes:
        content: Bytes of content.
        redirect: URL encoded path to redirect or None.

    Internal attributes:
        content_s: String of content. By default, it joins html_header,
            html_footer, head, and body.
        redirect_r: URL unencoded path to redirect or None.
        name: Pagename. Used for title.
    """

    redirect_r = None

    html_header = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">"""
    html_footer = "</html>"

    head_base = """<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<title>{name}</title>
</head>"""
    body = "<body></body>"

    pagename = ""

    dirfooter = """<p>
<form action=".go" method="get">
<a href=".hist">History</a>
|
Go or create page: <input type="text" name="name" value="" />
</form>
</p>"""

    pagefooter = """<hr />
<p>
<a href=".edit.{name}">Edit</a>
<a href=".hist.{name}">History</a>
|
<a href=".list">List</a>
</p>"""

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
            return urllib.parse.quote(self.redirect_r)

    @property
    def content(self):
        return self.content_s.encode("utf-8")

    @property
    def content_s(self):
        return "\n".join((self.html_header, self.head,
                        self.body, self.html_footer))

    @property
    def head(self):
        return self.head_base.format(name=self.pagename)

class NO_OP(OP):
    """Class used when path has no operator."""

    def __init__(self, file, path_):
        OP.__init__(self, file, path_)

        if file.isdir(path_):
            if not path_.path.endswith("/"):
                self.redirect_r = path_.base + "/"
                return
            try:
                c = file.load(path_) + self.pagefooter.format(name="index")
            except EnvironmentError as e:
                if e.errno != 2:
                    raise
                ls = file.listdir(path_)
                c = ("<h1>{path}</h1>\n".format(path=path_.path) +
                     "".join(
                        """<a href="{name}">{name}</a><br />\n""".format(name=i)
                        for i in ls) +
                     self.dirfooter)
        else:
            try:
                c = file.load(path_) + self.pagefooter.format(name=path_.base)
            except EnvironmentError as e:
                if e.errno == 2:
                    self.redirect_r = ".edit." + path_.base
                    return
                else:
                    raise
        self.body = "\n".join(("<body>", c, "</body>"))
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
        data: Data to post. Directly passed from server."""
    try:
        op = importlib.import_module("dowwner.op." + path_.op)
    except ImportError:
        raise
    try:
        return op.OP_POST(file, path_, data)
    except AttributeError:
        raise
