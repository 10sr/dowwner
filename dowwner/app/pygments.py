from pygments.formatters import get_formatter_by_name

from .apps import DowwnerConfig

FORMAT = "html"
classname = DowwnerConfig.dowwner_pygments_class


def get_css(style: str) -> str:
    fmter = get_formatter_by_name(FORMAT, style=style)
    css = fmter.get_style_defs(f".{classname}")
    assert isinstance(css, str)
    return css
