#!/usr/bin/env python3

"""Manage history."""

import dowwner.op

class ContentGET(dowwner.op.BaseContent):
    histfooter = """<a href="{name}">{name}</a>"""
    baklink = """<a href=".bak.{name}">{name}</a><br />\n"""

    def main(self):
        ls = self.storage.lshist(self.path)
        self.content = ("<h1>hist: {path}</h1>\n".format(path=self.path.path) +
                        "".join(self.baklink.format(name=i) for i in ls))

        self.navigation = self.histfooter.format(name=(self.path.base or "./"))
        self.pagename = "hist: " + self.path.path
        return
