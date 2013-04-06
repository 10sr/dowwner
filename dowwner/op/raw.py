#!/usr/bin/env python3

import dowwner.op

class ContentGET(dowwner.op.BaseContent):
    """Go class."""
    def __init__(self, file, path_, wikiname):
        """
        Args:
            file: File object.
            path_: Path object.
        """
        dowwner.op.BaseContent.__init__(self, file, path_, wikiname)

        self.content_raw = file.load(path_, raw=True)
        self.type = "text/plain"
        return
