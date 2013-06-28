#!/usr/bin/env python3

import dowwner.op

class ContentGET(dowwner.op.BaseContent):
    """Go class."""
    def main(self):
        self.content_raw = self.storage.load((self.path.dir, self.path.base))
        self.type = "text/plain; charset=utf-8"
        self.mtime = self.storage.getmtime((self.path.dir, self.path.base))
        return
