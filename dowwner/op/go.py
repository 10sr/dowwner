#!/usr/bin/env python3

import dowwner.op

class ContentGET(dowwner.op.BaseContent):
    """Go class."""
    def main(self):
        try:
            self.redirect_r = self.path.query["name"][0]
        except KeyError:
            self.redirect_r = None
        return
