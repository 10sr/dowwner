#!/usr/bin/env python3

import os
import shutil
from time import strftime

class File():
    """File and directory handler."""

    FILE_SUFFIX = ".md"
    __md = None

    def __init__(self, rootdir):
        self.rootdir = os.path.realpath(rootdir)
        return

    def __gen_fullpath(self, pathstr):
        """Return fullpath from path string. FILE_SUFFIX is not appended.

        Args:
            dir: True to return dir of path_."""
        # note: normpath always strip last "/"
        fpath = os.path.normpath(os.path.join(self.rootdir,
                                              pathstr.lstrip("/")))
        # fpath must be under rootdir for security reason.
        assert fpath.startswith(self.rootdir)
        return fpath

    def isdir(self, path_):
        "Return True if path_ is dir."
        return os.path.isdir(self.__gen_fullpath(path_.path))

    def listdir(self, path_):
        "Return list of files in path_. Do not check if path_ is dir."
        items = ["./", "../"]
        fullpath = self.__gen_fullpath(path_.path)
        for l in os.listdir(fullpath):
            if l.startswith("."):
                continue
            elif os.path.isdir(os.path.join(fullpath, l)):
                items.append(l + "/")
            elif l.endswith(self.FILE_SUFFIX):
                items.append(os.path.splitext(l)[0])
        return items

    def __read_file(self, path_):
        if self.isdir(path_):
            p = os.path.join(self.__gen_fullpath(path_.path),
                             "index" + self.FILE_SUFFIX)
        else:
            p = self.__gen_fullpath(path_.path) + self.FILE_SUFFIX
        with open(p, encoding="utf-8") as f:
            return f.read()

    def __md2html(self, s):
        if self.__md is None:
            from dowwner.markdown import Markdown
            self.__md = Markdown()
        return self.__md.convert(s)

    def load(self, path_, raw=False):
        """Load file.

        if path_ is dir, try to load "index" file.

        Args:
            path_: Path object.
            raw: False to convert to html.

        Raises:
            EnvironmentError
        """
        s = self.__read_file(path_)
        if raw:
            return s
        else:
            return self.__md2html(s)

    def save(self, path_, data):
        """Save file with data.

        Args:
            path_: Path object.
            data: String of data.
        """
        fullpath = self.__gen_fullpath(path_.path) + self.FILE_SUFFIX
        try:
            os.makedirs(os.path.dirname(fullpath))
        except OSError as e:
            if e.errno != 17: # 17 means file exists
                raise
        self.backup(path_)
        with open(fullpath,
                  mode="w", encoding="utf-8") as f:
            f.write(data)
            return True
        return False

    def rm(self, path_):
        """Remove page.

        Returns:
            Path of dirname.
        """
        self.backup(path_)
        os.remove(self.__gen_fullpath(path_.path) + self.FILE_SUFFIX)
        return path_.dir

    @staticmethod
    def __current_time():
        return strftime("%Y%m%d_%H%M%S")

    def __backup_gen_fullpath(self, path_):
        """Generate and return fullpath of target for backup,
        which is like /full/path/.bak.20130216_193548.name.md .
        """
        timestr = self.__current_time()
        fpath = self.__gen_fullpath(os.path.join(path_.dir,
                                                 (".bak." + timestr + "." +
                                                  path_.base +
                                                  self.FILE_SUFFIX)))
        return fpath

    def backup(self, path_):
        """Backup file.

        This should be called everytime files are modified or deleted.
        Path for backup is generated by self.__backup_gen_fullpath .
        """
        # todo: this method should be operated atomic way
        if path_.base == "":
            raise PageNameError("{}: Cannot backup directory".format(rpath))

        origpath = self.__gen_fullpath(path_.path) + self.FILE_SUFFIX
        newpath = self.__backup_gen_fullpath(path_)
        try:
            shutil.copyfile(origpath, newpath)
        except EnvironmentError as e:
            if e.errno != 2:
                raise
        return

    # methods for history handling

    def lshist(self, path_):
        l = []
        prefix = ".bak."
        suffix = ("." + path_.base + self.FILE_SUFFIX) if path_.base else ""
        neg_suffix_len = len(self.FILE_SUFFIX) * (-1)
        for f in os.listdir(self.__gen_fullpath(path_.dir)):
            if (f.startswith(prefix) and f.endswith(suffix)):
                l.append(f[:neg_suffix_len])
        l.sort(reverse=True)
        return l

    def load_bak(self, path_, raw=False):
        """Load backed up file."""
        fulldir = self.__gen_fullpath(path_.dir)
        fullpath = os.path.join(fulldir,
                                ".bak." + path_.base + self.FILE_SUFFIX)
        with open(fullpath, encoding="utf-8") as f:
            s = f.read()

        if raw:
            return s
        else:
            return self.__md2html(s)
        return
