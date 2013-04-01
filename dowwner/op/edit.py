#!/usr/bin/env python3

from os import path

from dowwner import exc
import dowwner.op

# todo: use stylesheet for scale.

class OP_GET(dowwner.op.OP):
    """Editor class."""

    _content = """<h1>{path}</h1>
<form action=".save.{name}" method="post">
<p>
<input type="submit" name="submit" value="submit" />
</p>
<p>
<textarea type="content" name="content" value="content" rows="24" cols="80">
{origtext}</textarea>
</p>
</form>"""

    def __init__(self, file, path_, wikiname, orig=None, target=None):
        """
        Args:
            file: File object.
            path_: Path object.
        """
        dowwner.op.OP.__init__(self, file, path_, wikiname)

        if path_.isstyle:
            orig = file.load_style(path_)
        elif orig is None:
            try:
                orig = file.load(path_, True)
            except exc.PageNotFoundError:
                orig = ""

        if target is None:
            target = path_.base

        self.content = self._content.format(path=path_.path,
                                            origtext=orig,
                                            name=target)
        self.pagename = "edit: " + path_.path
        return
