#!/usr/bin/env python3

import dowwner.op.edit

class ContentGET(dowwner.op.edit.ContentGET):
    """Revert class."""
    def __init__(self, file, path_, wikiname):
        """
        Args:
            file: File object.
            path_: Path object.
        """
        orig = file.load_bak(path_, raw=True)
        dowwner.op.edit.ContentGET.__init__(self, file, path_, wikiname, orig,
                                            target=path_.base.partition(".")[2])
        self.pagename = "revert: " + path_.path
        return
