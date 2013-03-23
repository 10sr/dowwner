#!/usr/bin/env python3

from os import path

import dowwner.op

# todo: use stylesheet for scale.

class OP_GET(dowwner.op.OP):
    """Editor class."""
    def __init__(self, file, path_, orig=None):
        """
        Args:
            file: File object.
            path_: Path object.
        """
        dowwner.op.OP.__init__(self, file, path_)

        ls = file.listdir(path_)
        c = ("<h1>{path}</h1>\n".format(path=path_.path) +
             "".join("""<a href="{name}">{name}</a><br />\n""".format(name=i)
                     for i in ls) +
             self.dirfooter)

        self.body = "\n".join(("<body>", c, "</body>"))
        return
