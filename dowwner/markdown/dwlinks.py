#!/usr/bin/env python

import markdown


class DWLinkExtension(markdown.Extension):
    def extendMarkdown(self, md, md_globals):
        pat = DWLinks(r"\[\[([\w0-9_ -/.]+)\]\]")
        md.inlinePatterns.add("dwlink", pat, "<not_strong")
        return


class DWLinks(markdown.inlinepatterns.Pattern):
    def handleMatch(self, m):
        if m.group(2).strip():
            url = m.group(2).strip()
            a = markdown.util.etree.Element('a')
            a.text = url
            a.set('href', url)
        else:
            a = ''
        return a


def makeExtension(configs=tuple()):
    return DWLinkExtension(configs=configs)
