#!/usr/bin/env python3

from os import path

from dowwner import exc
import dowwner.op

class ContentGET(dowwner.op.BaseContent):
    """Editor class."""

    _content = """<h1>{path}</h1>
<form action=".save.{name}" method="post">
<p>
<input type="submit" name="submit" value="submit" />
</p>
<p>
<textarea type="content" name="content" value="content" rows="24" cols="80" style="width:95%;">
{origtext}</textarea>
</p>
</form>"""

    def main(self, orig=None, target=None):
        if self.path.isstyle:
            dtype = "style"
        else:
            dtype = None

        if orig is None or self.path.isstyle:
            try:
                orig = self.storage.load((self.path.dir, self.path.base), dtype)
            except exc.PageNotFoundError:
                orig = ""

        if target is None:
            target = self.path.base
        if self.path.isstyle:
            target = target + ".css"

        self.content = self._content.format(path=self.path.path,
                                            origtext=orig,
                                            name=target)
        self.pagename = "edit: " + self.path.path
        return
