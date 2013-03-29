#!/usr/bin/env python3

import urllib
from cgi import FieldStorage

import dowwner.op

class OP_POST(dowwner.op.OP):
    def __init__(self, file, path_, wikiname, data):
        dowwner.op.OP.__init__(self, file, path_, wikiname)

        if isinstance(data, FieldStorage):
            content = data.getfirst("content").replace("\r", "")
        else:
            data2 = urllib.parse.parse_qs(data.decode(), keep_blank_values=True)
            content = data2["content"][0].replace("\r", "")

        if path_.base.endswith(self.STYLE_SUFFIX):
            file.save_style(path_, content)
            self.redirect_r = "./"
        elif content == "":
            file.rm(path_)
            self.redirect_r = ".list"
        else:
            file.save(path_, content)
            self.redirect_r = path_.base

        return
