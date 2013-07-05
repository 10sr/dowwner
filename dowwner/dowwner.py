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
        self.__md = None
        return

    def get(self, pathstr, query, cachetime=None):
        """Return content object for request handler.

        Args:
            pathstr: String of path
            query: String of query
            cachetime: time string of if-modified-since
        """
        p = Path(pathstr, query)
        return dowwner.op.get(self.storage, p, self.name, self.md2html,
                              (self.__str2time(cachetime) if cachetime else 0))

    def post(self, pathstr, query, data):
        """Return content object for request handler.

        Args:
            pathstr: String of path
            query: String of query
            data: data to post
        """
        p = Path(pathstr, query)
        return dowwner.op.post(self.storage, p, self.name, self.md2html, data)

    def md2html(self, mdstr):
        if self.__md is None:
            from dowwner.markdown import Markdown
            self.__md = Markdown()
        else:
            self.__md.reset()
        return self.__md.convert(mdstr)

    @staticmethod
    def __time2str(t):
        """Convert epoch time into HTTP time string."""
        return time.strftime("%a, %d %b %Y %H:%M:%S %Z", time.gmtime(t))

    @staticmethod
    def __str2time(s):
        """Convert HTTP time string into epoch time."""
        return time.mktime(time.strptime(s, "%a, %d %b %Y %H:%M:%S %Z"))

    def req_http(self, met, *args, **kargs):
        """Handle http request.

        Returns:
            Tuple of (status, message, redirect, headers, content).
        """
        # TODO: use correct http status code for redirect
        headers = dict()
        try:
            c = getattr(self, met.lower())(*args, **kargs)

        except (exc.DowwnerBaseException, Exception) as e:
            if isinstance(e, exc.PageNotModified):
                status = 304
                message = "Not modified"
                content = None
                redirect = None

            elif isinstance(e, exc.Redirection):
                status = e.status
                message = e.short
                redirect = e.url
                content = bytes(str(e), encoding="utf-8")

            else:
                if isinstance(e, exc.PageNameError):
                    status = 404
                    message = e.short
                else:
                    status = 500
                    message = "Internal server error"

                redirect = None
                if self.debug:
                    content = b"".join((
                        b"<pre><code>",
                        html.escape(
                            "".join(format_exception(
                                *sys.exc_info()))).encode("utf-8"),
                        b"</code></pre>"))
                else:           # not self.debug
                    content = message.encode("utf-8")

                logger = logging.getLogger(__name__)
                logger.exception(message)

                headers["Content-Type"] = "text/html; charset=utf-8"


        else:                   # no exception
            content = bytes(c)
            status = 200
            message = "OK"
            redirect = None

            headers["Content-Type"] = c.type
            if c.mtime is not None:
                headers["Last-Modified"] = self.__time2str(c.mtime)
            if c.filename:
                headers["Content-Disposition"] = (
                    "attachment;" +
                    "filename={}".format(c.filename))

        if content:
            headers["Content-Length"] = str(len(content))
        # print((status, message, redirect, headers, content))
        return (status, message, redirect, headers, content)

    def verify_addr(self, addr):
        return addr == "127.0.0.1"
