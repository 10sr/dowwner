#!/usr/bin/env python3

from __future__ import absolute_import

import os
import sys
import time
from traceback import format_exception
import html
import logging

from dowwner.path import Path
from dowwner.storage.file import File
import dowwner.op
from dowwner import exc

import locale
locale.setlocale(locale.LC_TIME, "C")
os.environ["TZ"] = "GMT+00"
time.tzset()

class Dowwner():
    """Dowwner main class."""

    def __init__(self, rootdir, debug=False):
        self.storage = File(rootdir)
        self.name = os.path.basename(rootdir)
        self.debug = debug
        return

    def get(self, pathstr, query):
        """Return content object for request handler."""
        p = Path(pathstr, query)
        return dowwner.op.get(self.storage, p, self.name)

    def post(self, pathstr, query, data):
        """Return content object for request handler."""
        p = Path(pathstr, query)
        return dowwner.op.post(self.storage, p, self.name, data)

    @staticmethod
    def __time2str(t):
        return time.strftime("%a, %d %b %Y %H:%M:%S %Z", time.gmtime(t))

    @staticmethod
    def __str2time(s):
        return

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
            if self.debug:
                content = b"".join((
                    b"<pre><code>",
                    html.escape(
                        "".join(format_exception(
                            *sys.exc_info()))).encode("utf-8"),
                    b"</code></pre>"))
            else:
                content = message.encode("utf-8")
            headers["Content-Type"] = "text/html; charset=utf-8"
            redirect = None

            logger = logging.getLogger(__name__)
            logger.exception(message)

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
            if c.mtime is not None:
                headers["Last-Modified"] = self.__time2str(c.mtime)
            if c.filename:
                headers["Content-Disposition"] = (
                    "attachment;" +
                    "filename={}".format(c.filename))

        headers["Content-Length"] = str(len(content))
        return (status, message, redirect, headers, content)

    def verify_addr(self, addr):
        return addr == "127.0.0.1"
