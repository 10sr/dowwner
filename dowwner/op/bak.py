#!/usr/bin/env python3

import dowwner.op

class OP_GET(dowwner.op.OP):
    """Editor class."""

    bakfooter = """<hr />
<p>
<a href="{name}">Current</a>
<a href=".revert.{name}">Revert</a>
|
<a href=".list">List</a>
</p>
"""

    def __init__(self, file, path_, orig=None):
        """
        Args:
            file: File object.
            path_: Path object.
        """
        dowwner.op.OP.__init__(self, file, path_)

        c = (file.load_bak(path_) +
             self.bakfooter.format(name=path_.base.rpartition(".")[2]))
        self.body = "\n".join(("<body>", c, "</body>"))
        return
