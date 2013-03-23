#!/usr/bin/env python3

from os import path

import dowwner.op

# todo: use stylesheet for scale.

_body = """
<body>
<h1>{path}</h1>
<form action=".save.{name}" method="post">
<p><input type="submit" name="submit" value="submit" /></p>
<p>
<textarea type="content" name="content" value="content" rows="24" cols="80">
{origtext}</textarea>
</p>
</form>
</body>
"""

class OP_GET(dowwner.op.OP):
    """Editor class."""
    def __init__(self, file, path_, orig=None, target=None):
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

        if target is None:
            target = path_.base

        self.body = _body.format(path=path_.path,
                                 origtext=orig,
                                 name=target)
        return
