#!/usr/bin/env python3

import os.path

import dowwner.op

class ContentGET(dowwner.op.BaseContent):
    """arch class."""

    def main(self):
        """
        Args:
            storage: Storage object.
            path_: Path object.
        """
        if self.path.path == "/":
            basename = self.wikiname
        else:
            basename = (self.wikiname + "-" +
                        os.path.basename(self.path.path.rstrip("/")))
        self.filename = basename + ".zip"

        self.content_bytes = self.storage.zip(self.path)
        self.type = "application/zip"
        # self.redirect_raw = "."
        return
