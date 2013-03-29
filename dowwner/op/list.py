#!/usr/bin/env python3

import dowwner.op

class OP_GET(dowwner.op.NO_OP):
    """List class."""
    def __init__(self, file, path_, wikiname):
        """
        Args:
            file: File object.
            path_: Path object.
        """
        dowwner.op.OP.__init__(self, file, path_, wikiname)
        self.init_as_list()
        return
