#!/usr/bin/env python3

from __future__ import absolute_import

import os
import sys

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
        message = None

        try:
            c = getattr(self, met.lower())(*args, **kargs)
        except Exception as e:
            if isinstance(e, exc.PageNameError):
                status = 404
            else:
                status = 500
            content = b"".join((
                b"<pre><code>",
                "".join(format_exception(*sys.exc_info())).encode(),
                b"</code></pre>"))
        else:
            content = bytes(c)
            redirect = c.redirect
            if redirect:
                status = 303
            else:
                status = 200

        headers = dict()
        headers["Content-Type"] = c.type
        if c.filename:
            headers["Content-Disposition"] = ("attachment;" +
                                              "filename={}".format(c.filename))
        headers["Content-Length"] = len(content)
        return (status, message, redirect, headers, content)

    def verify_addr(self, addr):
        return addr == "127.0.0.1"
