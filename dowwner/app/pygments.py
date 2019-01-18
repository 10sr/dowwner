from typing import Optional

import pygments
from pygments.formatters import get_formatter_by_name
from pygments.util import ClassNotFound

from .apps import DowwnerConfig

_FORMAT = "html"
_classname = DowwnerConfig.dowwner_pygments_class

pygments_version = pygments.__version__


def get_css(style: str) -> Optional[str]:
    # May raise ClassNotFound error
    try:
        fmter = get_formatter_by_name(_FORMAT, style=style)
    except ClassNotFound:
        return None
    css = fmter.get_style_defs(f".{_classname}")
    assert isinstance(css, str)
    return css
