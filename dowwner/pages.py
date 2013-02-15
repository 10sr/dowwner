#!/usr/bin/env python3

import os
path = os.path

FILE_SUFFIX = ".md"

class _Page():
    """Content object for request handler.

    Attributes:
        path: Relative path for content.
        exists: True if content exists.
        content: Bytes of content.
    """

    def __init__(self, pages, rpath):
        """
        Args:
            pages: Pages object.
            rpath: Path relative to rootdir.
        """
        self.pages = pages
        self.dir = pages.dir
        self.path = rpath
        self.exists = True
        try:
            self.content = self.pages.get_content(self.path).encode()
        except OSError as e:
            print(e)
            if e.errno == 2:    # No such file or directory
                self.content = b""
                self.exists = False
            else:
                raise
        return

    # @property
    # def exists(self):
    #     return self.pages.exists(self.path)

    # @property
    # def content(self):
    #     """Return content in bytes."""

class Pages():
    def __init__(self, rootdir):
        self.dir = rootdir
        return

    def get(self, rpath):
        """Return page object for request handler.

        Args:
            path_: Path.
        """
        return _Page(self, rpath)

    def post(self, rpath, content):
        """Post data.

        Args:
            rpath: relative path to save.
            content: string of content.
        """
        print(rpath)
        print(content)
        fullpath = self.gen_fullpath(rpath + FILE_SUFFIX)
        try:
            os.makedirs(path.dirname(fullpath))
        except OSError as e:
            if e.errno != 17: # 17 means file exists
                raise
        with open(fullpath,
                  mode="w", encoding="utf-8") as f:
            f.write(content)
            return True
        return False

    def verify_addr(self, addr):
        return addr == "127.0.0.1"

    def gen_fullpath(self, rpath):
        fpath = path.normpath(path.join(self.dir, rpath))
        # fpath must be under rootdir for security reason.
        assert fpath.startswith(self.dir)
        return fpath

    def get_content(self, rpath):
        """
        Args:
            rpath: Relative path.

        Returns:
            Content string.

        Raises:
            OSError: File not found.
        """
        print(rpath)
        fpath = self.gen_fullpath(rpath)
        if path.isdir(fpath):
            return self.__load_dir(fpath, rpath)
        else:
            return self.__load_file(fpath)

    def __load_dir(self, fpath, rpath):
        inputbox = """
<p>
<form action=".get/{path}" method="get">
Move or create page: <input type="text" name="pagename" value="" />
</form>
</p>
"""
        items = []
        for l in os.listdir(fpath):
            if l.startswith("."):
                continue
            elif path.isdir(path.join(fpath, l)):
                items.append(l + "/")
            elif l.endswith(FILE_SUFFIX):
                items.append(path.splitext(l)[0])

        return ("<h1>dir.</h1>" +
                "<br />".join(items) +
                inputbox.format(path=rpath))

    def __load_file(self, fpath):
        with open(fpath + FILE_SUFFIX) as f:
            return f.read()
