#!/usr/bin/env python3

import os
import urllib

class Path():
    """
    Path object.

    This object only treats path as string, and does not know its contents.
    Path elements can be accessed in list-like way. For example,
        >>> p = Path("/dir/file")
        >>> p[0]
        "dir"
        >>> p[1]
        "file"

    Attributes:
        origpath: Original path. Starts with "/".
        op: Operator. "/dir/.op.file" -> "op", "/dir/.list" -> "list",
            "/dir/file" -> "".
        path: Page path. Starts with "/".
        query: Dict of query parameters in url.
        dir: Dirname of path.
        base: Basename of path.
    """
    def __init__(self, path_):
        """
        Args:
            path_: Path relative to root directory. Starts with "/" and quoted
                using parse.quote().
        """
        o = urllib.parse.urlparse(path_)
        path_ = o.path
        self.origpath_quoted = path_
        self.origpath = urllib.parse.unquote(path_, encoding="utf-8")

        query_r = o.query
        self.query = urllib.parse.parse_qs(query_r)

        elems = path_.split("/")
        # "/" -> ["", ""]
        # "/a" -> ["", "a"]
        # "/.edit.a" -> ["", ".edit.a"]
        # "/dir/" -> ["", "dir", ""]
        # "/dir/.edit.f" -> ["", "dir", ".edit.f"]

        if elems[-1].startswith("."):
            self.op, sep, base = elems[-1][1:].partition(".")
            self.elems = elems[1:-1] + [base]
            self.path = "/" + "/".join(self.elems)
        else:
            self.op = ""
            self.path = self.origpath
            self.elems = elems[1:]

        self.dir, self.base = os.path.split(self.path)
        return

    def __getitem__(self, idx):
        return self.elems[idx]

    def __str__(self):
        return str(self.__dict__)

if __name__ == "__main__":
    def test():
        p1 = Path("/dir/file")
        print(p1.__dict__)
        p2 = Path("/dir/.op.file")
        print(p2.__dict__)
        p3 = Path("/dir/.list")
        print(p3.__dict__)
        print(p3[0])
        return

    test()
