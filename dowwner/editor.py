#!/usr/bin/env python3

# todo: use stylesheet for scale.

_formstr = """
<h1>{path}</h1>
<form action="/.save/{path}" method="post">
<p><input type="submit" name="submit" value="submit" /></p>
<p>
<textarea type="content" name="content" value="content" rows="24" cols="80">
</textarea>
</p>
</form>
"""

class Editor():
    """Editor class.

    Attributes:
        rpath: Relative path.
        content: bytes of editor code.
    """
    def __init__(self, rpath):
        """
        Args:
            path_: Relative path."""
        self.path = rpath
        self.content = _formstr.format(path=rpath).encode()
        return
