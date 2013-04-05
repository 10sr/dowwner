#!/usr/bin/env python3

import dowwner.op

class OP_GET(dowwner.op.OP):
    """Go class."""
    def __init__(self, file, path_, wikiname):
        """
        Args:
            file: File object.
            path_: Path object.
        """
        dowwner.op.OP.__init__(self, file, path_, wikiname)

        self.content_raw = file.load(path_, raw=True)
        self.type = "text/plain"
        return
