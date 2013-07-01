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
            self.__query_search(query)
        else:
            raise Exception("{}: Invalid query type".format(t))
        return

    def __query_search(self, query):
        search_result = self.storage.search(query, self.path.dir)
        self.content = (
            "<ul>\n" +
            "\n".join(
                """<li><a href="{0}">{0}</a>: {1}</li>""".format(e[0], e[1])
                for e in search_result
            ) +
            "</ul>\n"
        )
        return
