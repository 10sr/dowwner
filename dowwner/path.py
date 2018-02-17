#!/usr/bin/env python3

import posixpath
try:
    from urllib import parse as urlparse
except ImportError:
    import urlparse

from dowwner import exc


class Path():
    """
    Path object.

    This object only treats path as string, and does not know its contents.
    If any elems in self.path starts with ".", raise exc.PageNameError
    If any elems in self.dir ends with self.STYLE_SUFFIX, raise
    exc.PageNameError.
    If pathstr ends with the suffix ".css", the suffix is removed and isstyle
    is set to True.
    If basename of pathstr is in COMMON_SUFFIX, its dirname is always ignored.

    Attributes:
        origpath: Original path. Starts with "/".
        op: Operator. "/dir/.op.file" -> "op", "/dir/.list" -> "list",
            "/dir/file" -> "".
        path: Page path. Starts with "/".
        query: Dict of query parameters in url.
        dir: Dirname of path.
        base: Basename of path.
        base_orig: Basename with operator.
        isstyle: True if path has style suffix.

    Raises:
        dowwner.exc.PageNameError
    """

    COMMON_FILES = ("common.css",)
    STYLE_SUFFIX = ".css"

    def __init__(self, pathstr, query):
        """
        Args:
            pathstr: Path relative to root directory. Starts with "/" and
                quoted with parse.quote().
            query: String of query. Passed to patse_qs
        """
        # o = urlparse.urlparse(path_)
        # path_ = o.path
        # self.origpath_quoted = path_
        # self.origpath = urlparse.unquote(path_, encoding="utf-8")

        # query_r = o.query
        # self.query = urlparse.parse_qs(query_r)
        self.origpath_quoted = pathstr
        self.origpath = urlparse.unquote(pathstr, encoding="utf-8")
        self.query = urlparse.parse_qs(query, encoding="utf-8")

        self.dir, self.base_orig = posixpath.split(self.origpath)

        if self.base_orig.startswith("."):
            self.op, dotsep, self.base = self.base_orig[1:].partition(".")
        else:
            self.op = ""
            self.base = self.base_orig

        if self.base in self.COMMON_FILES:
            self.dir = "/"

        self.isstyle = self.base.endswith(self.STYLE_SUFFIX)
        if self.isstyle:
            self.base = self.base[:-4]  # remove ".css"
            if self.base == "":
                raise exc.PageNameError("css suffix with no name")

        self.path = posixpath.join(self.dir, self.base)
        if self.STYLE_SUFFIX + "/" in self.path:
            raise exc.PageNameError("Stylesheet suffix in dirname")
        if "/." in self.path:
            raise exc.PageNameError("Dot file or directory in path")
        return

    def __str__(self):
        return str(self.__dict__)


if __name__ == "__main__":
    def test():
        p1 = Path("/dir/file")
        print(p1)
        p2 = Path("/dir/.op.file")
        print(p2)
        p3 = Path("/dir/.list")
        print(p3)
        return

    test()
