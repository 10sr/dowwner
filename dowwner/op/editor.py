#!/usr/bin/env python3

from os import path

import dowwner.op

# todo: use stylesheet for scale.

_formstr = """
<h1>{path}</h1>
<form action=".save.{name}" method="post">
<p><input type="submit" name="submit" value="submit" /></p>
<p>
<textarea type="content" name="content" value="content" rows="24" cols="80">
{origtext}</textarea>
</p>
</form>
"""

class Editor(dowwner.op.OP):
    """Editor class."""
    def __init__(self, file, path_, orig=None):
        """
        Args:
            file: File object.
            path_: Path object.
        """
        dowwner.op.OP.__init__(self, file, path_)

        if orig is None:
            try:
                orig = file.load(path_, True)
            except EnvironmentError as e:
                if e.errno == 2:    # No such file or directory
                    orig = ""
                else:
                    raise

        self.content_s = _formstr.format(path=path_.path,
                                       origtext=origtext,
                                       name=path_.base)
        return
