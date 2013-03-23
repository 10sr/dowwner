#!/usr/bin/env python3

class Saver():
    pass

class _PostPage(_Page):
    def __init__(self, pages, rpath, data):
        self.pages = pages
        rpath = urllib.parse.unquote(rpath)
        self.path = rpath

        elems = rpath.split("/")
        for i in elems[:-1]:
            # if any item other than last one starts with "."
            if i.startswith("."):
                raise PageNameError("Invalid page name: {}".format(rpath))

        assert elems[-1].startswith(".save.")
        realrpath ="/".join(elems[:-1] + [elems[-1].replace(".save.", "", 1)])

        data2 = urllib.parse.parse_qs(data.decode(), keep_blank_values=True)
        content = data2["content"][0].replace("\r", "")
        if content == "":
            self.pages.rm(realrpath)
            self._redirect = path.dirname(realrpath)
        else:
            self.pages.write_data(realrpath, content)
            self._redirect = realrpath

        return
