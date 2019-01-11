#!/usr/bin/env python3

from pygments.formatters import get_formatter_by_name

FORMAT = "html"
style = "default"
classname = ".codehilite"

fmter = get_formatter_by_name(FORMAT, style=style)
print(fmter.get_style_defs(classname))
