#!/usr/bin/env python3

import os
try:
    from urllib import parse as urlparse
except ImportError:
    import urlparse

# todo: prohibit any directory name ends with ".css"

class Path():
    """
    Path object.

    This object only treats path as string, and does not know its contents.

    Attributes:
        origpath: Original path. Starts with "/".
        op: Operator. "/dir/.op.file" -> "op", "/dir/.list" -> "list",
            "/dir/file" -> "".
        path: Page path. Starts with "/".
        query: Dict of query parameters in url.
        dir: Dirname of path.
        base: Basename of path.
        base_orig: Basename with operator.
    """
    def __init__(self, path_):
        """
        Args:
            path_: Path relative to root directory. Starts with "/" and quoted
                with parse.quote().
        """
        o = urlparse.urlparse(path_)
        path_ = o.path
        self.origpath_quoted = path_
        self.origpath = urlparse.unquote(path_, encoding="utf-8")

        query_r = o.query
        self.query = urlparse.parse_qs(query_r)

        self.dir, self.base_orig = os.path.split(path_)

        if self.base_orig.startswith("."):
            self.op, dotsep, self.base = self.base_orig[1:].partition(".")
        else:
            self.op = ""
            self.base = self.base_orig

        self.path = os.path.join(self.dir, self.base)
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
