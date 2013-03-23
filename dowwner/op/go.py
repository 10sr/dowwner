#!/usr/bin/env python3

import dowwner.op

class OP_GET(dowwner.op.OP):
    """Editor class."""
    def __init__(self, file, path_, orig=None):
        """
        Args:
            file: File object.
            path_: Path object.
        """
        dowwner.op.OP.__init__(self, file, path_)

        self.redirect_r = path_.query["name"][0]
        return
