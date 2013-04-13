#!/usr/bin/env python3

from __future__ import absolute_import

import os
import sys
from traceback import format_exception
import html

from dowwner.path import Path
from dowwner.container.file import File
import dowwner.op
from dowwner import exc

class Dowwner():
    """Dowwner main class."""

    COMMON_FILES = ("common.css",)

    def __init__(self, rootdir):
        self.container = File(rootdir, self.COMMON_FILES)
        self.name = os.path.basename(rootdir)
        return

    def get(self, pathstr, query):
        """Return OP object for request handler."""
        p = Path(pathstr, query)
        return dowwner.op.get(self.container, p, self.name)

    def post(self, pathstr, query, data):
        """Return OP object for request handler."""
        p = Path(pathstr, query)
        return dowwner.op.post(self.container, p, self.name, data)

    def req_http(self, met, *args, **kargs):
        """Handle http request.

        Returns:
            Tuple of (status, message, redirect, headers, content).
        """
        # todo: use correct http status code for redirect
        headers = dict()
        try:
            c = getattr(self, met.lower())(*args, **kargs)

        except Exception as e:
            if isinstance(e, exc.PageNameError):
                status = 404
                message = e.short
            else:
                status = 500
                message = "Internal server error"
            content = b"".join((
                b"<pre><code>",
                html.escape("".join(format_exception(*sys.exc_info()))).encode(),
                b"</code></pre>"))
            headers["Content-Type"] = "text/html; charset=utf-8"
            redirect = None

        else:
            content = bytes(c)
            redirect = c.redirect
            if redirect:
                status = 303
                message = "See Other"
            else:
                status = 200
                message = "OK"

            headers["Content-Type"] = c.type
            if c.filename:
                headers["Content-Disposition"] = (
                    "attachment;" +
                    "filename={}".format(c.filename))

        headers["Content-Length"] = str(len(content))
        return (status, message, redirect, headers, content)

    def verify_addr(self, addr):
        return addr == "127.0.0.1"
