#!/usr/bin/env python3

import os
import os.path
import shutil
from time import strftime

from dowwner import exc

class File():
    """File and directory handler."""

    FILE_SUFFIX = ".md"
    BAK_SUFFIX = ".bak"
    CONV_SUFFIX = ".html"
    CACHE_PREFIX = ".cache."
    __md = None

    def __init__(self, rootdir):
        self.rootdir = os.path.realpath(rootdir)
        return

    def __gen_fullpath(self, pathstr):
        """Return fullpath from path string."""
        # note: normpath always strip last "/"
        fpath = os.path.normpath(os.path.join(self.rootdir,
                                              pathstr.lstrip("/")))
        # fpath must be under rootdir for security reason.
        assert fpath.startswith(self.rootdir)
        return fpath

    def isdir(self, path_):
        "Return True if directory named path exists."
        return os.path.isdir(self.__gen_fullpath(path_.path))

    def listdir(self, path_):
        """Return list of files in path_. When dir not found, return []."""
        items = []
        fullpath = self.__gen_fullpath(path_.path)

        try:
            ls = os.listdir(fullpath)
        except EnvironmentError as e:
            if e.errno == 2:
                return items
            elif e.errno == 20:   # Not a directory
                raise
            else:
                raise

        for l in ls:
            if l.startswith("."):
                continue
            elif os.path.isdir(os.path.join(fullpath, l)):
                items.append(l + "/")
            elif l.endswith(self.FILE_SUFFIX):
                items.append(os.path.splitext(l)[0])
        return items

    def __md2html(self, s):
        if self.__md is None:
            from dowwner.markdown import Markdown
            self.__md = Markdown()
        return self.__md.convert(s)

    def load_style(self, path_):
        """Load css file and return as string.

        If css file not found, return empty string.
        If path_.base == "common.css", always return same content regardless of
        path_.dir .
        """

        assert path_.isstyle

        if path_.base == "common.css":
            fpath = self.__gen_fullpath("common.css")
        else:
            fpath = self.__gen_fullpath(path_.path)

        try:
            with open(fpath, encoding="utf-8") as f:
                c = f.read()
        except EnvironmentError as e:
            if e.errno == 2:
                c = ""
            else:
                raise

        return c

    def save_style(self, path_, data):
        """Save stylesheet."""
        assert path_.isstyle
        fpath = self.__gen_fullpath(path_.path)
        # todo: backup previous content
        with open(fpath, encoding="utf-8", mode="w") as f:
            f.write(data)
        return

    @staticmethod
    def __is_file_newer(f1, f2):
        """Return True if f1 exists and is newer than f2."""
        try:
            t2 = os.path.getmtime(f2)
        except EnvironmentError as e:
            if e.errno == 2:
                raise exc.PageNotFoundError("Invalid file name: {}".format(f2))
        try:
            t1 = os.path.getmtime(f1)
        except EnvironmentError as e:
            if e.errno == 2:
                return False
            else:
                raise
        return t1 >= t2

    def load(self, path_, raw=False):
        """Load file.

        If path_.path ends with slash, try to load "index" page.

        Args:
            path_: Path object.
            raw: False to convert to html. Used to get original text for edit
                page.

        Raises:
             dowwner.exc.PageNotFoundError
        """
        if path_.path.endswith("/"):
            fdir = self.__gen_fullpath(path_.dir)
            base = "index"
        else:
            fdir = self.__gen_fullpath(path_.dir)
            base = path_.base

        mdpath = os.path.join(fdir, base + self.FILE_SUFFIX)
        if raw:
            try:
                with open(mdpath, encoding="utf-8") as f:
                    s = f.read()
            except EnvironmentError as e:
                if e.errno == 2:
                    raise exc.PageNotFoundError
                else:
                    raise
            return s

        htmlpath = os.path.join(fdir,
                                self.CACHE_PREFIX + base + self.CONV_SUFFIX)
        if self.__is_file_newer(htmlpath, mdpath):
            # if cache exists use that.
            with open(htmlpath, encoding="utf-8") as f:
                html = f.read()
            return html

        try:
            with open(mdpath, encoding="utf-8") as f:
                md = f.read()
        except EnvironmentError as e:
            if e.errno == 2:
                raise exc.PageNotFoundError
            else:
                raise
        html = self.__md2html(md)
        pid = os.fork()
        if pid == 0:        # child
            # cache html
            with open(htmlpath, encoding="utf-8", mode="w") as f:
                f.write(html)
            os._exit(0)
        else:
            return html

    def save(self, path_, data):
        """Save file with data.

        This method creates all subdirectories if needed to save files.

        Args:
            path_: Path object.
            data: String of data.
        """
        if self.isdir(path_):
            pathstr = os.path.join(path_.path, "index" + self.FILE_SUFFIX)
        else:
            pathstr = path_.path + self.FILE_SUFFIX
        fullpath = self.__gen_fullpath(pathstr)

        try:
            os.makedirs(os.path.dirname(fullpath))
        except OSError as e:
            if e.errno != 17: # 17 means file exists
                raise
        self.__backup(path_)
        with open(fullpath,
                  mode="w", encoding="utf-8") as f:
            f.write(data)
            return True
        return False

    def rm(self, path_):
        """Remove page. Do nothing if path_ not exists.

        Returns:
            Path of dirname.
        """
        try:
            self.__backup(path_)
            os.remove(self.__gen_fullpath(path_.path) + self.FILE_SUFFIX)
        except EnvironmentError as e:
            if e.errno == 2:
                pass
            else:
                raise
        return path_.dir

    # methods for history handling

    @staticmethod
    def __current_time():
        return strftime("%Y%m%d_%H%M%S")

    def __backup_gen_fullpath(self, path_):
        """Generate and return fullpath of target for backup,
        which is like /full/path/.20130216_193548.name.md.bak .
        """
        timestr = self.__current_time()
        fpath = self.__gen_fullpath(os.path.join(path_.dir,
                                                 ("." + timestr + "." +
                                                  path_.base +
                                                  self.FILE_SUFFIX +
                                                  self.BAK_SUFFIX)))
        return fpath

    def __backup(self, path_):
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

    def lshist(self, path_):
        """Return list of history files.

        Values returned are used for self.load_bak().
        """
        l = []

        suffix = self.FILE_SUFFIX + self.BAK_SUFFIX
        neg_suffix_len = len(suffix) * (-1)
        if path_.base:
            suffix = "." + path_.base + suffix

        try:
            ls = os.listdir(self.__gen_fullpath(path_.dir))
        except EnvironmentError as e:
            if e.errno == 20:
                return []
            else:
                raise

        for f in os.listdir(self.__gen_fullpath(path_.dir)):
            if f.endswith(suffix):
                l.append(f[1:neg_suffix_len]) # remove first dot and suffixes
        l.sort(reverse=True)

        return l

    def load_bak(self, path_, raw=False):
        """Load backed up file.

        Basename of path_ is decided by the return of self.lshist().

        Raises:
            dowwner.exc.PageNameError
        """
        fulldir = self.__gen_fullpath(path_.dir)
        fullpath = os.path.join(fulldir,
                                ("." + path_.base +
                                 self.FILE_SUFFIX + self.BAK_SUFFIX))
        try:
            with open(fullpath, encoding="utf-8") as f:
                s = f.read()
        except EnvironmentError as e:
            if e.errno == 2:
                raise exc.PageNameError
            else:
                raise
        if raw:
            return s
        else:
            return self.__md2html(s)
        return
