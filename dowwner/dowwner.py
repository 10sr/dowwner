#!/usr/bin/env python3

from __future__ import absolute_import

import os

from dowwner.path import Path
from dowwner.container.file import File
import dowwner.op

class Dowwner():
    """Dowwner main class."""

    COMMON_FILES = ("common.css",)

    def __init__(self, rootdir):
        self.container = File(rootdir, self.COMMON_FILES)
        self.name = os.path.basename(rootdir)
        return

    def get(self, pathstr, query):
        """Return OP object for request handler.

        Args:
            rpath: Path queried.
        """
        p = Path(pathstr, query)
        return dowwner.op.get(self.container, p, self.name)

    def post(self, pathstr, query, data):
        """Return OP object for request handler.

        Args:
            rpath: Path queried.
        """
        p = Path(pathstr, query)
        return dowwner.op.post(self.container, p, self.name, data)

    def verify_addr(self, addr):
        return addr == "127.0.0.1"
