#!/usr/bin/env python3

import dowwner.op

class ContentGET(dowwner.op.BaseContent):
    """Go class."""
    def main(self):
        """
        Args:
            storage: Storage object.
            path_: Path object.
        """
        self.content_raw = self.storage.load(self.path, raw=True)
        self.type = "text/plain; charset=utf-8"
        self.mtime = self.storage.getmtime(self.path)
        return
