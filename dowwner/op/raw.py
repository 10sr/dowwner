#!/usr/bin/env python3

import dowwner.op

class ContentGET(dowwner.op.BaseContent):
    """Go class."""
    def main(self):
        """
        Args:
            file: File object.
            path_: Path object.
        """
        self.content_raw = self.file.load(self.path, raw=True)
        self.type = "text/plain; charset=utf-8"
        return
