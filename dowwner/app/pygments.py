from typing import Optional

import pygments
from pygments.formatters import get_formatter_by_name
from pygments.util import ClassNotFound

_FORMAT = "html"

pygments_version = pygments.__version__


def get_css(style: str, classname: str) -> Optional[str]:
    try:
        fmter = get_formatter_by_name(_FORMAT, style=style)
    except ClassNotFound:
        return None
    css = fmter.get_style_defs(f".{classname}")
    assert isinstance(css, str)
    return css
