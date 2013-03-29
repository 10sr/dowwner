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

        try:
            self.redirect_r = path_.query["name"][0]
        except KeyError:
            self.redirect_r = None
        return
