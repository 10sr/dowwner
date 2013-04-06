#!/usr/bin/env python3

"""Manage history."""

import dowwner.op

class ContentGET(dowwner.op.BaseContent):
    histfooter = """<a href="{name}">{name}</a>"""
    baklink = """<a href=".bak.{name}">{name}</a><br />\n"""

    def __init__(self, file, path_, wikiname):
        dowwner.op.BaseContent.__init__(self, file, path_, wikiname)

        ls = file.lshist(path_)
        self.content = ("<h1>hist: {path}</h1>\n".format(path=path_.path) +
                        "".join(self.baklink.format(name=i) for i in ls))

        self.navigation = self.histfooter.format(name=(path_.base or "./"))
        self.pagename = "hist: " + path_.path
        return
