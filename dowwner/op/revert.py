#!/usr/bin/env python3

import dowwner.op.edit

class OP_GET(dowwner.op.edit.OP_GET):
    """Editor class."""
    def __init__(self, file, path_):
        """
        Args:
            file: File object.
            path_: Path object.
        """
        orig = file.load_bak(path_, raw=True)
        dowwner.op.edit.OP_GET.__init__(self, file, path_, orig,
                                        target=path_.base.partition(".")[2])
        return
