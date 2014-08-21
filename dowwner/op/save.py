#!/usr/bin/env python3

import urllib
from cgi import FieldStorage

import dowwner.op
from dowwner import exc


class ContentPOST(dowwner.op.BaseContent):
    def main(self):
        if self.path.isstyle:
            dtype = "style"
        else:
            dtype = None

        if isinstance(self.data, FieldStorage):
            content = self.data.getfirst("content").replace("\r", "")
        else:
            data = urllib.parse.parse_qs(self.data.decode(),
                                         keep_blank_values=True)
            content = data["content"][0].replace("\r", "")

        if content == "":
            try:
                self.storage.rm((self.path.dir, self.path.base), dtype=dtype)
            except exc.PageNameError:
                pass
            raise exc.SeeOtherRedirection(".list")
        else:
            self.storage.save((self.path.dir, self.path.base), content,
                              dtype=dtype)
            if self.path.isstyle:
                raise exc.SeeOtherRedirection("./")
            else:
                raise exc.SeeOtherRedirection(self.path.base)

        return
