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
        content_s: String of content.
        redirect_r: URL unencoded path to redirect or None.
    """

    html_header = ""
    html_footer = ""

    content_s = ""
    redirect_r = None

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

class NO_OP(OP):
    """Class used when path has no operator."""
    def __init__(self, file, path_):
        OP.__init__(self, file, path_)
        if file.isdir(path_):
            if not path_.path.endswith("/"):
                self.redirect_r = path_.path + "/"
                return
            c = "<br />".join(file.listdir(path_))
        else:
            c = file.load(path_)
        self.content_s = "".join((self.html_header, c, self.html_footer))
        return

def get(file, path_):
    if path_.op == "":
        return NO_OP(file, path_)
    else:
        try:
            op = importlib.import_module(path_.op, "dowwner.op")
        except ImportError:
            raise
        try:
            return op.OP_GET(file, path_)
        except:
            raise

def post(file, path_):
    try:
        op = importlib.import_module(path_.op, "dowwner.op")
    except ImportError:
        raise
    try:
        return op.OP_POST(file, path_)
    except:
        raise
