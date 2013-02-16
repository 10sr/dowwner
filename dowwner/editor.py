#!/usr/bin/env python3

# todo: use stylesheet for scale.

_formstr = """
<h1>{path}</h1>
<form action="/.save/{path}" method="post">
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
        content: bytes of editor code.
    """
    def __init__(self, pages, rpath):
        """
        Args:
            pages: Pages object.
            rpath: Relative path.
        """
        self.path = rpath
        self.pages = pages
        try:
            self.origtext = self.pages.get_content(rpath, True)
        except EnvironmentError as e:
            if e.errno == 2:    # No such file or directory
                self.origtext = ""
            else:
                raise
        self.content = _formstr.format(path=rpath,
                                       origtext=self.origtext).encode()
        return
