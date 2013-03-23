#!/usr/bin/env python3

# todo: manage history

import os
path = os.path
import urllib

from dowwner.path import Path
from dowwner.file import File
from dowwner import op as dop
from dowwner.exc import PageNameError

class Dowwner():
    """Dowwner main class."""
    def __init__(self, rootdir):
        self.file = File(rootdir)
        return

    def get(self, rpath):
        """Return OP object for request handler.

        Args:
            rpath: Path queried.
        """
        p = Path(rpath)
        try:
            return dop.get(self.file, p)
        except ImportError:
            raise PageNameError("Invalid page naem: {}".format(rpath))

    def post(self, rpath, data):
        """Return OP object for request handler.

        Args:
            rpath: Path queried.
        """
        p = Path(rpath)
        try:
            return dop.post(self.file, p, data)
        except ImportError:
            raise PageNameError("Invalid page naem: {}".format(rpath))

    def verify_addr(self, addr):
        return addr == "127.0.0.1"
