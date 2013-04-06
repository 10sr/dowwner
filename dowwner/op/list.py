#!/usr/bin/env python3

import dowwner.op

class ContentGET(dowwner.op.DefContent):
    """List class."""
    def __init__(self, file, path_, wikiname):
        """
        Args:
            file: File object.
            path_: Path object.
        """
        dowwner.op.BaseContent.__init__(self, file, path_, wikiname)
        self.init_as_list()
        return
