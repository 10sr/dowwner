# TODO: Which package to put this file?

import re

import markdown
from markdown.extensions.wikilinks import WikiLinkExtension

import markdown2

from .apps import DowwnerConfig

# TODO: Any way to strip [[]] from display text?
_LINK_PATTERNS = [(re.compile(r"\[\[([\w0-9_ -/.]+)\]\]"), r"\1")]


def _to_html_markdown2(source: str) -> str:
    result = markdown2.markdown(
        source, extras=["link-patterns"], link_patterns=_LINK_PATTERNS
    )
    assert isinstance(result, str)
    return result


def _to_html_Markdown(source: str) -> str:
    result = markdown.markdown(
        # Cannot have slashes inside of blackets
        source,
        extensions=[
            WikiLinkExtension(base_url="", end_url="", html_class="dowwner-wikilink"),
            "fenced_code",
            "codehilite",
        ],
        extension_configs={
            "codehilite": {"css_class": DowwnerConfig.dowwner_pygments_class}
        },
        output_format="html5",
    )
    assert isinstance(result, str)
    return result


to_html = _to_html_Markdown
