#!/usr/bin/env python3

from urllib import parse as urlparse

class Path():
    """
    Path object.

    Attributes:
        origpath: Original path. Starts with "/".
        op: Operator.
        path: Page path.
        full: Fullpath.
    """
    def __init__(self, path_):
        """
        Args:
            path_: Path relative to root directory. Starts with "/" and quoted
                using parse.quote().
        """
        self.origpath_quoted = path_
        self.origpath = urlparse.unquote(path_)

        elems = path_.split("/")
        # "/" -> ["", ""]
        # "/a" -> ["", "a"]
        # "/.edit.a" -> ["", ".edit.a"]
        # "/dir/" -> ["", "dir", ""]
        # "/dir/.edit.f" -> ["", "dir", ".edit.f"]
        for i in elems[:-1]:
            if i.startswith("."):
                raise PageNameError("Invalid page name: {}".format(
                        self.origpath))

        if elems[-1].startswith("."):
            self.op, sep, base = elems[-1][1:].partition(".")
            self.path = "/".join(elems[:-1] + [base])
        else:
            self.op = ""
            self.path = self.origpath
        return

if __name__ == "__main__":
    def test():
        p1 = Path("/dir/file")
        print(p1.__dict__)
        p2 = Path("/dir/.op.file")
        print(p2.__dict__)
        return

    test()
