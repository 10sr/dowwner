#!/usr/bin/env python3

from __future__ import absolute_import

import os

from dowwner.path import Path
from dowwner.file import File
from dowwner import op as dop

class Dowwner():
    """Dowwner main class."""

    COMMON_FILES = ("common.css",)

    def __init__(self, rootdir):
        self.file = File(rootdir, self.COMMON_FILES)
        self.name = os.path.basename(rootdir)
        return

    def get(self, rpath):
        """Return OP object for request handler.

        Args:
            rpath: Path queried.
        """
        p = Path(rpath)
        return dop.get(self.file, p, self.name)

    def post(self, rpath, data):
        """Return OP object for request handler.

        Args:
            rpath: Path queried.
        """
        p = Path(rpath)
        return dop.post(self.file, p, self.name, data)

    def verify_addr(self, addr):
        return addr == "127.0.0.1"
