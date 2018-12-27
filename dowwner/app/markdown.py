# TODO: Which package to put this file?

import markdown2

def to_html(markdown: str) -> str:
    return markdown2.markdown(markdown)
