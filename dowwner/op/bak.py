#!/usr/bin/env python3

import dowwner.op

class OP_GET(dowwner.op.OP):
    """bak class."""

    baknav = """<p>
<a href="{basename}">Current</a>
<a href=".revert.{name}">Revert</a>
|
<a href=".list">List</a>
</p>"""

    def __init__(self, file, path_, wikiname, orig=None):
        """
        Args:
            file: File object.
            path_: Path object.
        """
        dowwner.op.OP.__init__(self, file, path_, wikiname)

        self.content = file.load_bak(path_)
        self.navigation = self.baknav.format(
            basename=path_.base.rpartition(".")[2],
            name=path_.base)
        self.pagename = "bak: " + path_.path
        return
