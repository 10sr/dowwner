#!/usr/bin/env python3

"""Manage history."""

import dowwner.op

class OP_GET(dowwner.op.OP):
    histfooter = """<hr />
<a href="{name}">{name}</a>"""

    def __init__(self, file, path_):
        dowwner.op.OP.__init__(self, file, path_)

        ls = file.lshist(path_)
        c = ("<h1>{path}</h1>\n".format(path=path_.path) +
             "".join("""<a href="{name}">{name}</a><br />\n""".format(name=i)
                     for i in ls))

        f = self.histfooter.format(name=(path_.base or "./"))

        self.body = "\n".join(("<body>", c, f, "</body>"))
        return