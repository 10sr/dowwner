#!/usr/bin/env python3

"""Manage history."""

import dowwner.op

class OP_GET(dowwner.op.OP):
    def __init__(self, file, path_):
        dowwner.op.OP.__init__(self, file, path_)
        ls = file.lshist(path_)
        c = ("<h1>{path}</h1>\n".format(path=path_.path) +
             "".join("""<a href="{name}">{name}</a><br />\n""".format(name=i)
                     for i in ls))

        self.body = "\n".join(("<body>", c, "</body>"))
        return
