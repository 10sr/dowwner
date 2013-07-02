#!/usr/bin/env python3

import os
import os.path
from time import strftime

from dowwner import exc
from dowwner import storage

class File(storage.BaseStorage):
    """File and directory Storage handler."""

    FILE_SUFFIX = ".md"
    STYLE_SUFFIX = ".css"
    BAK_SUFFIX = ".bak"
    CONV_SUFFIX = ".html"
    CACHE_PREFIX = ".cache."
    LIST_FILE = ".list"

    __search_func = None

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

    def isdir(self, pathstr):
        "Return True if directory named path exists."
        return os.path.isdir(self.__gen_fullpath(pathstr))

    def __gen_pagepath(self, patht, dtype=None):
        """Return string of page path."""
        if dtype == "style":
            return os.path.join(self.__gen_fullpath(patht[0]),
                                patht[1] + self.STYLE_SUFFIX)
        elif dtype:
            return os.path.join(self.__gen_fullpath(patht[0]),
                                ".".join(("", dtype, patht[1])))
        else:
            return os.path.join(self.__gen_fullpath(patht[0]),
                                patht[1] + self.FILE_SUFFIX)

    def listdir(self, pathstr):
        """Return list of pages in pathstr. When dir not found, return []."""
        items = []
        fullpath = self.__gen_fullpath(pathstr)

        if not self.isdir(pathstr):
            return []

        try:
            with open(os.path.join(fullpath, self.LIST_FILE)) as fo:
                ls = fo.read().splitlines()
        except EnvironmentError as e:
            if e.errno != 2:
                raise
            else:
                pass
        else:
            return [f for f in ls if f]

        # Try again after making list. If failed again, consider directory not
        # found and return empty list.
        self.__update_list(pathstr)
        try:
            with open(os.path.join(fullpath, self.LIST_FILE)) as fo:
                ls = fo.read().splitlines()
        except EnvironmentError as e:
            if e.errno == 2:
                return []
            else:
                raise
        else:
            return [f for f in ls if f]

    def load(self, patht, dtype=None):
        """Load data.

        Args:
            patht: Tuple of path like (dir, base).
            dtype: String of type of data.

        Returns:
            String of content.

        Raises:
             dowwner.exc.PageNotFoundError
             dowwner.exc.NotADirectoryError
        """
        fpath = self.__gen_pagepath(patht, dtype)
        try:
            with open(fpath, encoding="utf-8") as f:
                s = f.read()
        except EnvironmentError as e:
            if e.errno == 2:
                raise exc.PageNotFoundError(
                    "{}/{}: No such page".format(*patht))
            elif e.errno == 20:
                raise exc.NotADirectoryError
            else:
                raise
        return s

    def __update_list(self, relpath):
        """Create .list files recursively."""
        fullpath = self.__gen_fullpath(relpath)

        try:
            ls = os.listdir(fullpath)
        except EnvironmentError as e:
            if e.errno == 2:
                if relpath == "/":
                    return
                else:
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

    def save(self, patht, data, dtype=None):
        """Save file with data.

        This method creates all subdirectories if needed to save files.
        After new file is created this method update ".list" of the directory
        and parent directories.

        Args:
            patht: Tuple of path like (dir, base).
            data: String of data.
            dtype: String representing type of data.
        """
        fpath = self.__gen_pagepath(patht, dtype)

        try:
            os.makedirs(os.path.dirname(fpath))
        except OSError as e:
            if e.errno != 17: # 17 means file exists
                raise

        file_existed = os.access(fpath, os.F_OK)

        with open(fpath, mode="w", encoding="utf-8") as f:
            f.write(data)

        if dtype:
            # if not ordinal page
            return True

        if not file_existed:
            self.__update_list(patht[0])

        pid = os.fork()
        if pid == 0:            # child
            self.__backup(patht)
            os._exit(0)
        return True

    def rm(self, patht, dtype=None):
        """Remove page.

        Raises:
            dowwner.exc.PageNotFoundError
        """
        try:
            os.remove(self.__gen_pagepath(patht, dtype))
        except EnvironmentError as e:
            if e.errno == 2:
                raise exc.PageNotFoundError(
                    "{}/{}: No such page".format(*patht))
            else:
                raise
        self.__update_list(patht[0])
        return

    def getmtime(self, patht, dtype=None):
        """Get last modified time. If not available return None."""
        fpath = self.__gen_pagepath(patht, dtype)

        try:
            return os.stat(fpath).st_mtime
        except OSError as e:
            if e.errno == 2:
                return None
                # if self.isdir(os.path.join(*patht)):
                #     return None
                # else:
                #     raise exc.PageNotFoundError(
                #         "{}/{}: Page not found".format(*patht))
            else:
                raise

    # methods for history handling

    @staticmethod
    def __current_time():
        return strftime("%Y%m%d_%H%M%S")

    def __backup_gen_fullpath(self, patht):
        """Generate and return fullpath of target for backup,
        which is like /full/path/.20130216_193548.name.md.bak .
        """
        timestr = self.__current_time()
        fpath = self.__gen_fullpath(os.path.join(patht[0],
                                                 ("." + timestr + "." +
                                                  patht[1] +
                                                  self.FILE_SUFFIX +
                                                  self.BAK_SUFFIX)))
        return fpath

    def __backup(self, patht):
        """Backup file.

        This should be called everytime files are modified.
        Path for backup is generated by self.__backup_gen_fullpath .

        Returns:
            Fullpath of backup file or None if no file to backup.

        Raises:
            dowwner.exc.PageNameError: patht indicates directory.
        """
        # todo: this method should be operated atomic way
        if patht[1] == "":
            raise exc.PageNameError(
                "{}: Cannot backup directory".format(patht[0]))

        newpath = self.__gen_pagepath(patht)

        try:
            with open(newpath, mode="rb") as f:
                newb = f.read()
        except EnvironmentError as e:
            if e.errno == 2:
                raise exc.PageNotFoundError(
                    "{}/{}: Page not found".format(*patht))
            else:
                raise

        try:
            latestbase = self.lshist(patht)[0]
        except IndexError:
            latestpath = None
        else:
            latestpath = os.path.join(self.__gen_fullpath(patht[0]),
                                      "".join((".", latestbase,
                                               self.FILE_SUFFIX,
                                               self.BAK_SUFFIX)))

        if latestpath:
            with open(latestpath, mode="rb") as f:
                latestb = f.read()

            if newb == latestb:
                return None

        targetpath = self.__backup_gen_fullpath(patht)
        with open(targetpath, mode="wb") as f:
            f.write(newb)
        return newpath

    def lshist(self, patht):
        """Return list of history files.

        Returns:
            If patht indicates directory, returns the list of names of backups
            of all files in that directory. Otherwise, returns those of the
            file of patht.
            Values returned are used to load backup file with self.load_bak().
        """
        l = []

        suffix = self.FILE_SUFFIX + self.BAK_SUFFIX
        neg_suffix_len = len(suffix) * (-1)
        if patht[1]:
            suffix = "." + patht[1] + suffix

        try:
            ls = os.listdir(self.__gen_fullpath(patht[0]))
        except EnvironmentError as e:
            if e.errno == 20:
                return []
            else:
                raise

        for f in os.listdir(self.__gen_fullpath(patht[0])):
            if f.endswith(suffix):
                l.append(f[1:neg_suffix_len]) # remove first dot and suffixes
        l.sort(reverse=True)                  # latest first

        return l

    def load_bak(self, patht):
        """Load backed up file.

        patht[1] is decided by the return of self.lshist().

        Returns:
            String of content of patht.

        Raises:
            dowwner.exc.PageNameError
        """
        fulldir = self.__gen_fullpath(patht[0])
        fullpath = os.path.join(fulldir,
                                "".join((".", patht[1], self.FILE_SUFFIX,
                                         self.BAK_SUFFIX)))
        try:
            with open(fullpath, encoding="utf-8") as f:
                s = f.read()
        except EnvironmentError as e:
            if e.errno == 2:
                raise exc.PageNameError("{}/{}: No such page".format(*patht))
            else:
                raise
        return s

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

    def zip(self, pathstr):
        """Create zip archive for dir pathstr and return archive file as bytes."""
        if not self.isdir(pathstr):
            raise PageNameError("{}: Not a directory name".format(pathstr))
        ls = self.__ls_recursive(pathstr)
        # print(ls)
        oldpwd = os.getcwd()
        try:
            os.chdir(os.path.join(self.__gen_fullpath(pathstr),
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

    def search(self, word, pathstr, listall=False):
        if self.__search_func is None:
            if os.system("sh -c 'grep --help' >/dev/null 2>&1") == 0:
                self.__search_func = self.__search_grep
            else:
                self.__search_func = self.__search_native
        return self.__search_func(word, pathstr, listall)

    def __search_grep(self, word, pathstr, listall=False):
        from subprocess import Popen, PIPE
        fulldirpath = self.__gen_fullpath(pathstr)
        files1 = self.listdir(pathstr)

        # first check page name
        files2 = []
        for f in files1:
            if word in f:
                yield [f, ""]
            else:
                files2.append(f)

        if listall:
            files2 = files1
        files3 = [os.path.join(fulldirpath, e + self.FILE_SUFFIX)
                 for e in files2 if not e.endswith("/")]

        grep_command = ["grep", "--with-filename", "--line-number"]
        if not listall:
            grep_command.append("--max-count=1")
        grep_p = Popen(grep_command + [word] + files3, stdout=PIPE, stderr=PIPE)
        grep_result = grep_p.communicate()[0].decode("utf-8")
        for line in grep_result.splitlines():
            if not line:
                continue
            f, sep, line = line.partition(":")
            num, sep, line = line.partition(":")
            yield [os.path.basename(f)[:-3], line]
        raise StopIteration

    def __search_native(self, word, pathstr, listall=False):
        fulldirpath = self.__gen_fullpath(pathstr)
        for e in self.listdir(pathstr):
            if word in e:
                yield [e, ""]
                if not listall:
                    continue
            if e.endswith("/"):
                continue
            fullpath = os.path.join(fulldirpath, e + self.FILE_SUFFIX)
            with open(fullpath) as f:
                for line in f:
                    if word in line:
                        yield [e, line]
                        if not listall:
                            break
        raise StopIteration
