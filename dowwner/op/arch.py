#!/usr/bin/env python3

import os.path

import dowwner.op

class OP_GET(dowwner.op.OP):
    """arch class."""

    def __init__(self, file, path_, wikiname):
        """
        Args:
            file: File object.
            path_: Path object.
        """
        dowwner.op.OP.__init__(self, file, path_, wikiname)

        if path_.path == "/":
            basename = wikiname
        else:
            basename = wikiname + "-" + os.path.basename(path_.path.rstrip("/"))
        self.filename = basename + ".zip"

        self.content_bytes = file.zip(path_)
        self.type = "application/octet-stream"
        # self.redirect_raw = "."
        return
