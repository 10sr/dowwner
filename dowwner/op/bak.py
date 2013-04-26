#!/usr/bin/env python3

import dowwner.op

class ContentGET(dowwner.op.BaseContent):
    """bak class."""

    baknav = """<p>
<a href="{basename}">Current</a>
<a href=".revert.{name}">Revert</a>
|
<a href=".list">List</a>
</p>"""

    def main(self):
        """
        Args:
            storage: Storage object.
            path_: Path object.
        """
        self.content = self.storage.load_bak(self.path)
        self.navigation = self.baknav.format(
            basename=self.path.base.rpartition(".")[2],
            name=self.path.base)
        self.pagename = "bak: " + self.path.path
        return
