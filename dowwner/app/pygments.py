from pygments.formatters import get_formatter_by_name

FORMAT = "html"
classname = "codehilite"


def get_css(style: str) -> str:
    fmter = get_formatter_by_name(FORMAT, style=style)
    return fmter.get_style_defs(f".{classname}")
