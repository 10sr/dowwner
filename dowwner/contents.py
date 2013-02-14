#!/usr/bin/env python3

from os import path

_formstr = """
<form action="a.save" method="post">
<p>
name: <input type="text" name="namae" value="yuk" size="20" />
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

class _Content():
    """Content for request handler.

    Attributes:
        path: Path for content.
        fullpath: Fullpath for content.
        exists: True if content exists.
        content: Bytes of content.
    """

    def __init__(self, contents, path_):
        self.dir = contents.dir
        self.path = path_
        self.fullpath = path.normpath(path.join(self.dir, self.path))
        # path must be under rootdir for security reason.
        assert self.fullpath.startswith(self.dir)
        if self.path.endswith(".md"):
            self.exists = True
        else:
            self.exists = False
        self.content = (b"<em>dowwner</em><br />" +
                        self.fullpath.encode() +
                        _formstr.encode())
        return

class Contents():
    def __init__(self, rootdir):
        self.dir = rootdir
        return

    def get(self, path_):
        """Return content object for request handler.

        Args:
            path_: Path.
        """
        return _Content(self, path_)

    def post(self, path_, content):
        print(path_)
        print(content)
        return

    def verify_addr(self, addr):
        return addr == "127.0.0.1"
