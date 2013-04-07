#!/usr/bin/env python3

from os import path

from dowwner import exc
import dowwner.op

# todo: use stylesheet for scale.

class ContentGET(dowwner.op.BaseContent):
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

    def main(self, orig=None, target=None):
        """
        Args:
            file: File object.
            path_: Path object.
        """
        if orig is None or self.path.isstyle:
            try:
                orig = self.file.load(self.path, True)
            except exc.PageNotFoundError:
                orig = ""

        if target is None:
            target = self.path.base

        self.content = self._content.format(path=self.path.path,
                                            origtext=orig,
                                            name=target)
        self.pagename = "edit: " + self.path.path
        return
