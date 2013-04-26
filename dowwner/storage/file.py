#!/usr/bin/env python3

import os
import os.path
from time import strftime

from dowwner import exc

class File():
    """File and directory Storage handler."""

    FILE_SUFFIX = ".md"
    STYLE_SUFFIX = ".css"
    BAK_SUFFIX = ".bak"
    CONV_SUFFIX = ".html"
    CACHE_PREFIX = ".cache."
    LIST_FILE = ".list"

    __md = None

    def __init__(self, rootdir):
        """Initialize File.

        Args:
            rootdir: Root directory of files.
        """
        self.rootdir = os.path.realpath(rootdir)
        return

    def __gen_fullpath(self, pathstr):
        """Return fullpath from path string."""
        # note: normpath always strip last "/"
        base = os.path.basename(pathstr)
        fpath = os.path.normpath(os.path.join(self.rootdir,
                                              pathstr.lstrip("/")))
        # fpath must be under rootdir for security reason.
        assert fpath.startswith(self.rootdir)
        return fpath

    def isdir(self, path_):
        "Return True if directory named path exists."
        return os.path.isdir(self.__gen_fullpath(path_.path))

    def listdir(self, path_):
        """Return list of pages in path_. When dir not found, return []."""
        items = []
        fullpath = self.__gen_fullpath(path_.path)

        try:
            with open(os.path.join(fullpath, self.LIST_FILE)) as fo:
                ls = fo.read().splitlines()
        except EnvironmentError as e:
            if e.errno == 2:
                return []
            else:
                raise

        return [f for f in ls if f]

    def __md2html(self, s):
        if self.__md is None:
            from dowwner.markdown import Markdown
            self.__md = Markdown()
        return self.__md.convert(s)

    def load(self, path_, raw=False):
        """Load file.

        If path_.isstyle == True, always return raw contents of path_,
        otherwise return contents as html if raw == False.
        If path_.path ends with slash, try to load "index" page.

        Args:
            path_: Path object.
            raw: False to convert to html. Used to get original text for edit
                page.

        Returns:
            String of content.

        Raises:
             dowwner.exc.PageNotFoundError
             dowwner.exc.NotADirectoryError
        """
        if path_.isstyle:
            fpath = self.__gen_fullpath(path_.path) + self.STYLE_SUFFIX
            try:
                with open(fpath, encoding="utf-8") as f:
                    s = f.read()
            except EnvironmentError as e:
                if e.errno == 2:
                    raise exc.PageNotFoundError(
                        "{}: No such page".format(path_.path))
                else:
                    raise
            return s

        if path_.path.endswith("/"):
            base = "index" + self.FILE_SUFFIX
        else:
            base = path_.base + self.FILE_SUFFIX

        fdir = self.__gen_fullpath(path_.dir)
        mdpath = os.path.join(fdir, base)

        if raw:
            try:
                with open(mdpath, encoding="utf-8") as f:
                    s = f.read()
            except EnvironmentError as e:
                if e.errno == 2:
                    raise exc.PageNotFoundError(
                        "{}: No such page".format(path_.path))
                elif e.errno == 20:
                    raise exc.NotADirectoryError
                else:
                    raise
            return s

        try:
            with open(mdpath, encoding="utf-8") as f:
                md = f.read()
        except EnvironmentError as e:
            if e.errno == 2:
                raise exc.PageNotFoundError(
                    "{}: No such page".format(path_.path))
            else:
                raise
        return self.__md2html(md)

    def __update_list(self, relpath):
        """Create .list files recursively."""
        fullpath = self.__gen_fullpath(relpath)

        try:
            ls = os.listdir(fullpath)
        except EnvironmentError as e:
            if e.errno == 2:
                return self__update_list(self, os.path.join(relpath, ".."))
            elif e.errno == 20:   # Not a directory
                raise
            else:
                raise

        items = []
        for f in ls:
            if f.startswith(".") or f.startswith("_"):
                continue
            elif os.path.isdir(os.path.join(fullpath, f)):
                try:
                    with open(os.path.join(fullpath, f, self.LIST_FILE)) as fo:
                        if fo.read().strip(" \n"): # list file is not empty
                            items.append(f + "/")
                except EnvironmentError as e:
                    if e.errno == 2: # list file not exists
                        continue
                    else:
                        raise
            elif f.endswith(self.FILE_SUFFIX):
                items.append(os.path.splitext(f)[0])

        with open(os.path.join(fullpath, self.LIST_FILE), mode="w") as fo:
            fo.write("\n".join(items))

        # print(relpath)
        if relpath == "/":
            return
        else:
            return self.__update_list(os.path.normpath(os.path.join(relpath,
                                                                    "..")))

    def save(self, path_, data):
        """Save file with data.

        This method creates all subdirectories if needed to save files.
        After new file is created this method update ".list" of the directory
        and parent directories.

        Args:
            path_: Path object.
            data: String of data.
        """
        if self.isdir(path_):
            pathstr = os.path.join(path_.path, "index" + self.FILE_SUFFIX)
        elif path_.isstyle:
            pathstr = path_.path = self.STYLE_SUFFIX
        else:
            pathstr = path_.path + self.FILE_SUFFIX
        fullpath = self.__gen_fullpath(pathstr)

        try:
            os.makedirs(os.path.dirname(fullpath))
        except OSError as e:
            if e.errno != 17: # 17 means file exists
                raise

        file_existed = os.access(fullpath, os.F_OK)

        with open(fullpath, mode="w", encoding="utf-8") as f:
            f.write(data)

        if not file_existed:
            self.__update_list(path_.dir)

        pid = os.fork()
        if pid == 0:            # child
            self.__backup(path_)
            os._exit(0)
        return True

    def rm(self, path_):
        """Remove page.

        Raises:
            dowwner.exc.PageNotFoundError
        """
        try:
            os.remove(self.__gen_fullpath(path_.path) + self.FILE_SUFFIX)
        except EnvironmentError as e:
            if e.errno == 2:
                raise exc.PageNotFoundError(
                    "{}: No such page".format(path_.path))
            else:
                raise
        self.__update_list(path_.dir)
        return

    def getmtime(self, path_):
        if path_.isstyle:
            fullpath = self.__gen_fullpath(path_.path) + self.STYLE_SUFFIX
        else:
            # it is same logic used in load. should be in content class
            if path_.path.endswith("/"):
                base = "index" + self.FILE_SUFFIX
            else:
                base = path_.base + self.FILE_SUFFIX
            fdir = self.__gen_fullpath(path_.dir)
            fullpath = os.path.join(fdir, base)

        try:
            return os.stat(fullpath).st_mtime
        except OSError as e:
            if e.errno == 2:
                if self.isdir(path_):
                    return None
                else:
                    raise exc.PageNotFoundError(
                        "{}: Page not found".format(path_.path))
            else:
                raise

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

        This should be called everytime files are modified.
        Path for backup is generated by self.__backup_gen_fullpath .

        Returns:
            Fullpath of backup file or None if no file to backup.

        Raises:
            dowwner.exc.PageNameError: path_ indicates directory.
        """
        # todo: this method should be operated atomic way
        if path_.base == "":
            raise exc.PageNameError(
                "{}: Cannot backup directory".format(path_.path))

        newpath = self.__gen_fullpath(path_.path) + self.FILE_SUFFIX

        try:
            with open(newpath, mode="rb") as f:
                newb = f.read()
        except EnvironmentError as e:
            if e.errno == 2:
                raise exc.PageNotFoundError(
                    "{}: Page not found".format(path_.path))
            else:
                raise

        try:
            latestbase = self.lshist(path_)[0]
        except IndexError:
            latestpath = None
        else:
            latestpath = os.path.join(self.__gen_fullpath(path_.dir),
                                      "".join((".", latestbase,
                                               self.FILE_SUFFIX,
                                               self.BAK_SUFFIX)))

        if latestpath:
            with open(latestpath, mode="rb") as f:
                latestb = f.read()

            if newb == latestb:
                return None

        targetpath = self.__backup_gen_fullpath(path_)
        with open(targetpath, mode="wb") as f:
            f.write(newb)
        return newpath

    def lshist(self, path_):
        """Return list of history files.

        Returns:
            If path_ indicates directory, returns the list of names of backups
            of all files in that directory. Otherwise, returns those of the
            file of path_.
            Values returned are used to load backup file with self.load_bak().
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
        l.sort(reverse=True)                  # latest first

        return l

    def load_bak(self, path_, raw=False):
        """Load backed up file.

        Basename of path_ is decided by the return of self.lshist().

        Returns:
            String of content of path_, as html if raw == True.

        Raises:
            dowwner.exc.PageNameError
        """
        fulldir = self.__gen_fullpath(path_.dir)
        fullpath = os.path.join(fulldir,
                                "".join((".", path_.base, self.FILE_SUFFIX,
                                         self.BAK_SUFFIX)))
        try:
            with open(fullpath, encoding="utf-8") as f:
                s = f.read()
        except EnvironmentError as e:
            if e.errno == 2:
                raise exc.PageNameError("{}: No such page".format(path_.path))
            else:
                raise
        if raw:
            return s
        else:
            return self.__md2html(s)
        return

    def __ls_recursive(self, pathstr):
        l = []
        base = self.__gen_fullpath(pathstr)
        ls = os.listdir(base)
        for f in ls:
            fpath = os.path.join(base, f)
            if os.path.isdir(fpath):
                l.extend(self.__ls_recursive(os.path.join(pathstr, f)))
            elif ((not f.startswith(".") and f.endswith(self.FILE_SUFFIX)) or
                  f.endswith(".css")):
                l.append(os.path.join(pathstr, f))
        return l

    def zip(self, path_):
        """Create zip archive for dir path_ and return archive file as bytes."""
        if not self.isdir(path_):
            raise PageNameError("{}: Not a directory name".format(path_.path))
        ls = self.__ls_recursive(path_.path)
        # print(ls)
        oldpwd = os.getcwd()
        try:
            os.chdir(os.path.join(self.__gen_fullpath(path_.path),
                                  ".."))
            rells = (os.path.relpath(self.__gen_fullpath(f)) for f in ls)
            f = self.__zip_files(rells)
        finally:
            os.chdir(oldpwd)
        return f

    def __zip_files_python(self, files):
        """Zip given files with builtin python module."""
        from io import BytesIO
        from zipfile import ZipFile, ZIP_DEFLATED

        buf = BytesIO()
        try:
            # use deflate if available
            zf = ZipFile(buf, mode="w", compression=ZIP_DEFLATED)
        except RuntimeError:
            zf = ZipFile(buf, mode="w")

        for f in files:
            zf.write(f)

        zf.close()
        b = buf.getvalue()
        buf.close()
        return b

    def __zip_files(self, files):
        """Zip given files.

        Args:
            files: iterable of relative file path.

        Returns:
            Bytes of archive file.
        """
        l1 = list(files)
        from subprocess import Popen, PIPE
        try:
            ps = Popen(["zip", "-"] + l1, stdout=PIPE, stderr=PIPE)
            return ps.communicate()[0]
        except EnvironmentError as e:
            if e.errno == 2:
                return self.__zip_files_python(l1)
            else:
                raise

    # functions for cache

    def __gen_cachepath(self, path_):
        if self.isdir(path_):
            base = "index"
        else:
            base = path_.base
        return os.path.join(self.__gen_fullpath(path_.dir),
                            self.CACHE_PREFIX + base + self.CONV_SUFFIX)

    def save_cache(self, path_, data):
        with open(self.__gen_cachepath(path_), mode="w", encoding="utf-8") as f:
            f.write(data)
        return

    @staticmethod
    def __is_file_newer(f1, f2):
        """Return True if f1 exists and is same age newer than f2.

        Raises:
            dowwner.exc.PageNotFoundError: f2 not exists"""
        try:
            t2 = os.path.getmtime(f2)
        except EnvironmentError as e:
            if e.errno == 2:
                raise exc.PageNotFoundError("{}: No such file".format(f2))
        try:
            t1 = os.path.getmtime(f1)
        except EnvironmentError as e:
            if e.errno == 2:
                return False
            else:
                raise
        return t1 >= t2

    def load_cache(self, path_):
        cachepath = self.__gen_cachepath(path_)
        if self.isdir(path_):
            base = "index"
        else:
            base = path_.base
        fullpath = os.path.join(self.__gen_fullpath(path_.dir),
                                base + self.FILE_SUFFIX)

        if self.__is_file_newer(cachepath, fullpath):
            with open(cachepath, encoding="utf-8") as f:
                s = f.read()
        else:
            s = None
        return s