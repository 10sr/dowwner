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
    """

    html_header = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
"""
    html_footer = "</html>"

    head = "<head></head>"
    body = "<body></body>"

    redirect_r = None

    dirfooter = """
<p>
<form action=".get" method="get">
<a href=".hist">History</a>
|
Go or create page: <input type="text" name="pagename" value="" />
</form>
</p>
"""

    pagefooter = """
<hr />
<p>
<a href=".edit.{name}">Edit</a>
<a href=".hist.{name}">History</a>
|
<a href=".list">List</a>
</p>
"""

    def __init__(self, file, path_):
        """Initialize.

        Args:
            path_: Path object.
            file: File handler object.
        """
        self.path = path_
        self.file = file
        return

    @property
    def redirect(self):
        if self.redirect_r is None:
            return None
        else:
            return urllib.parse.quote(self.redirect_r)

    @property
    def content(self):
        return self.content_s.encode()

    @property
    def content_s(self):
        return "".join((self.html_header, self.head,
                        self.body, self.html_footer))

class NO_OP(OP):
    """Class used when path has no operator."""

    def __init__(self, file, path_):
        OP.__init__(self, file, path_)

        if file.isdir(path_):
            if not path_.path.endswith("/"):
                self.redirect_r = path_.path + "/"
                return
            ls = file.listdir(path_)
            c = ("<h1>{path}</h1>\n".format(path=path_.path) +
                 "".join(
                    """<a href="{name}">{name}</a><br />\n""".format(name=i)
                    for i in ls) +
                 self.dirfooter)
        else:
            c = file.load(path_) + self.pagefooter.format(name=path_.base)
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
        except:
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
    except:
        raise
