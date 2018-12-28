# TODO: Which package to put this file?

import re

import markdown
from markdown.extensions.wikilinks import WikiLinkExtension

import markdown2

# TODO: Any way to strip [[]] from display text?
_LINK_PATTERNS = [(re.compile(r"\[\[([\w0-9_ -/.]+)\]\]"), r"\1")]


def _to_html_markdown2(source: str) -> str:
    result = markdown2.markdown(
        source, extras=["link-patterns"], link_patterns=_LINK_PATTERNS
    )
    return str(result)


def _to_html_Markdown(source: str) -> str:
    result = markdown.markdown(
        # Cannot have slashes inside of blackets
        source,
        extensions=[WikiLinkExtension(base_url="", end_url="")],
        output_format="html5",
    )
    # For type checking
    return str(result)


to_html = _to_html_Markdown
