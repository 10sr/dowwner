#!/usr/bin/env python3

import urllib
from cgi import FieldStorage

import dowwner.op
from dowwner import exc

class ContentPOST(dowwner.op.BaseContent):
    def __init__(self, file, path_, wikiname, data):
        dowwner.op.BaseContent.__init__(self, file, path_, wikiname)

        if isinstance(data, FieldStorage):
            content = data.getfirst("content").replace("\r", "")
        else:
            data2 = urllib.parse.parse_qs(data.decode(), keep_blank_values=True)
            content = data2["content"][0].replace("\r", "")

        if content == "":
            try:
                file.rm(path_)
            except exc.PageNameError:
                pass
            self.redirect_r = ".list"
        else:
            file.save(path_, content)
            if path_.isstyle:
                self.redirect_r = "./"
            else:
                self.redirect_r = path_.base

        return
