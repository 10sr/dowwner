#!/usr/bin/env python3

_formstr = """
<form action="/.save/{path}" method="post">
<p>
name: <input type="text" name="namae" value="10sr" size="20" />
</p>
<p>
OS：
<input type="radio" name="OS" value="win" checked="checked" /> Windows
<input type="radio" name="OS" value="mac" /> Machintosh
<input type="radio" name="OS" value="unix" /> Unix
</p>
<p>
content: <br />
<textarea type="content" name="content" value="content"></textarea>
</p>
<p><input type="submit" name="submit" value="submit" /></p>
</form>
"""

class Editor():
    """Editor class.

    Attributes:
        path: Relative path.
        content: bytes of editor code.
    """
    def __init__(self, path_):
        """
        Args:
            path_: Relative path."""
        self.path = path_
        self.content = _formstr.format(path=path_).encode()
        return
