#!/usr/bin/env python3

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

        self.content_bytes = file.zip(path_)
        self.type = "application/octet-stream"
        self.filename = "dl.zip"
        # self.redirect_raw = "."
        return
