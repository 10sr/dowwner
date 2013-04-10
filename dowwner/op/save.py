#!/usr/bin/env python3

import urllib
from cgi import FieldStorage

import dowwner.op
from dowwner import exc

class ContentPOST(dowwner.op.BaseContent):
    def main(self):
        if isinstance(self.data, FieldStorage):
            content = self.data.getfirst("content").replace("\r", "")
        else:
            data = urllib.parse.parse_qs(self.data.decode(),
                                         keep_blank_values=True)
            content = data["content"][0].replace("\r", "")

        if content == "":
            try:
                self.file.rm(self.path)
            except exc.PageNameError:
                pass
            self.redirect_r = ".list"
        else:
            self.file.save(self.path, content)
            if self.path.isstyle:
                self.redirect_r = "./"
            else:
                self.redirect_r = self.path.base

        return
