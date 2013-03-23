#!/usr/bin/env python3

import urllib

import dowwner.op

class OP_POST(dowwner.op.OP):
    def __init__(self, file, path_, data):
        dowwner.op.OP.__init__(self, file, path_)

        data2 = urllib.parse.parse_qs(data.decode(), keep_blank_values=True)
        content = data2["content"][0].replace("\r", "")
        if content == "":
            file.rm(path_)
            print(path_)
            self.redirect_r = ".list"
        else:
            file.save(path_, content)
            self.redirect_r = path_.base

        return
