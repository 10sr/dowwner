#!/usr/bin/env python3

import dowwner.op

class ContentGET(dowwner.op.BaseContent):
    """Go class."""
    def main(self):
        try:
            t = self.path.query["t"][0]
        except KeyError:
            t = "Search"
        query = self.path.query["q"][0]

        if t == "Go":
            self.redirect_r = query
        elif t == "Search":
            self.content = query
        else:
            raise Exception("{}: Invalid query type".format(t))
        return
