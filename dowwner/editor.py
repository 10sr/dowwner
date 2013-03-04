#!/usr/bin/env python3

from os import path

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

class Editor():
    """Editor class.

    Attributes:
        rpath: Relative path.
        content: String of editor code.
    """
    def __init__(self, pages, rpath, orig=None):
        """
        Args:
            pages: Pages object.
            rpath: Relative path.
        """
        self.path = rpath
        self.pages = pages
        if orig is None:
            try:
                self.origtext = self.pages.get_raw_content(rpath)
            except EnvironmentError as e:
                if e.errno == 2:    # No such file or directory
                    self.origtext = ""
                else:
                    raise
        else:
            self.origtext = orig
        name = path.basename(rpath)
        self.content = _formstr.format(path=rpath,
                                       origtext=self.origtext,
                                       name=name)
        return
