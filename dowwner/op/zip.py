#!/usr/bin/env python3

import os.path

import dowwner.op

class ContentGET(dowwner.op.BaseContent):
    """arch class."""

    def main(self):
        """
        Args:
            file: File object.
            path_: Path object.
        """
        if path_.path == "/":
            basename = self.wikiname
        else:
            basename = (self.wikiname + "-" +
                        os.path.basename(self.path.path.rstrip("/")))
        self.filename = basename + ".zip"

        self.content_bytes = file.zip(self.path)
        self.type = "application/zip"
        # self.redirect_raw = "."
        return
