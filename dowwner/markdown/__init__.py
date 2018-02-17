#!/usr/bin/env python3

# [Extensions API — Python Markdo]
# (http://pythonhosted.org/Markdown/extensions/api.html)

import markdown

from dowwner.markdown import dwlinks


class Markdown(markdown.Markdown):
    def __init__(self):
        dwl = dwlinks.makeExtension()
        return markdown.Markdown.__init__(self,
                                          extensions=[dwl],
                                          output_format="xhtml1")


if __name__ == "__main__":
    pass
