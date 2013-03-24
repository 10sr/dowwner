#!/usr/bin/env python3

import dowwner.op

class OP_GET(dowwner.op.OP):
    """List class."""
    def __init__(self, file, path_):
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
        self.pagename = "list: " + path_.path
        return
