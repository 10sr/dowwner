#!/usr/bin/env python3

import os

class File():
    """File and directory handler."""

    FILE_SUFFIX = ".md"
    __md = None

    def __init__(self, rootdir):
        self.rootdir = os.path.realpath(rootdir)
        return

    def __gen_fullpath(self, path_):
        """Return fullpath from path object. FILE_SUFFIX is not appended."""
        # note: normpath always strip last "/"
        fpath = os.path.normpath(os.path.join(self.rootdir,
                                              path_.path.lstrip("/")))
        # fpath must be under rootdir for security reason.
        assert fpath.startswith(self.rootdir)
        return fpath

    def isdir(self, path_):
        "Return True if path_ is dir."
        return os.path.isdir(self.__gen_fullpath(path_))

    def listdir(self, path_):
        "Return list of files in path_. Do not check if path_ is dir."
        items = ["./", "../"]
        fullpath = self.__gen_fullpath(path_)
        for l in os.listdir(fullpath):
            if l.startswith("."):
                continue
            elif os.path.isdir(os.path.join(fullpath, l)):
                items.append(l + "/")
            elif l.endswith(self.FILE_SUFFIX):
                items.append(os.path.splitext(l)[0])
        return items

    def __read_file(self, path_):
        with open(self.__gen_fullpath(path_) + self.FILE_SUFFIX,
                  encoding="utf-8") as f:
            return f.read()

    def load(self, path_, raw=False):
        """Load file.

        Args:
            path_: Path object.
            raw: False to convert to html.

        Raises:
            EnvironmentError
        """
        s = self.__read_file(path_)
        if raw:
            return s

        if self.__md is None:
            from dowwner.markdown import Markdown
            self.__md = Markdown()
        return self.__md.convert(s)

    def save(self, path_, data):
        """Save file with data.

        Args:
            path_: Path object.
            data: String of data.
        """
        return

    def read_file(self, path_):
        return

    def write_file(self, path_):
        return

    def edit(self, rpath):
        """Return editor object for request handler."""
        return Editor(self, rpath)

    def rm(self, rpath):
        """Remove page.

        Returns:
            Path of dirname."""
        self.backup(rpath)
        os.remove(self.gen_fullpath(rpath) + self.FILE_SUFFIX)
        return path.dirname(rpath)

    def hist(self, rpath):
        """Get history file list."""
        return self.__hist.get(rpath)

    def backup(self, rpath):
        """Backup file.

        This should be called everytime files are modified or deleted.
        Backed up files are like .bak.20130216_193548.name
        """
        # todo: this method should be operated atomic way
        if rpath.endswith("/"):
            raise PageNameError("{}: Cannot backup directory".format(rpath))

        timestr = self.__current_time()
        dirname, basename = os.path.split(rpath)
        fulldir = self.pages.gen_fullpath(dirname)
        origpath = os.path.join(fulldir, basename + self.pages.FILE_SUFFIX)
        newpath = os.path.join(fulldir, ".bak." + timestr + "." +
                               basename + self.pages.FILE_SUFFIX)
        try:
            shutil.copyfile(origpath, newpath)
        except EnvironmentError as e:
            if e.errno != 2:
                raise
        return

    def __current_time(self):
        return strftime("%Y%m%d_%H%M%S")

    def write_data(self, rpath, content):
        """Post data.

        Args:
            rpath: relative path to save.
            content: string of content.
        """
        fullpath = self.gen_fullpath(rpath + self.FILE_SUFFIX)
        try:
            os.makedirs(path.dirname(fullpath))
        except OSError as e:
            if e.errno != 17: # 17 means file exists
                raise
        self.backup(rpath)
        with open(fullpath,
                  mode="w", encoding="utf-8") as f:
            f.write(content)
            return True
        return False

    def get_raw_content(self, rpath):
        fpath = self.gen_fullpath(rpath)
        return self.__read_file(fpath)

    def get_content(self, rpath):
        """
        Args:
            rpath: Relative path.

        Returns:
            Content string.

        Raises:
            OSError: File not found.
            dowwner.exc.PageNameError: Invalid page name.
            _DirWOLastSlash: dir without last slash.
        """
        fpath = self.gen_fullpath(rpath)

        if path.isdir(fpath):
            if not rpath.endswith("/"):
                raise _DirWOLastSlash()
            irpath = path.join(rpath, "index")
            try:
                return self.__gen_page_html(irpath)
            except EnvironmentError as e:
                if e.errno == 2:
                    return self.__gen_dir_html(fpath, rpath)
                else:
                    raise
        else:
            return self.__gen_page_html(rpath)

    def get_dir_content(self, rpath):
        fpath = self.gen_fullpath(rpath)
        return self.__gen_dir_html(fpath, rpath)

    def __gen_dir_html(self, fpath, rpath):
        inputbox = """
<p>
<form action=".get" method="get">
<a href=".hist">History</a>
|
Go or create page: <input type="text" name="pagename" value="" />
</form>
</p>
"""
        items = ["./", "../"]
        for l in os.listdir(fpath):
            if l.startswith("."):
                continue
            elif path.isdir(path.join(fpath, l)):
                items.append(l + "/")
            elif l.endswith(self.FILE_SUFFIX):
                items.append(path.splitext(l)[0])

        return ("<h1>{path}</h1>\n".format(path=rpath) +
                "<br />".join("""<a href="{name}">{name}</a>\n""".format(name=i)
                              for i in items) +
                inputbox)

    def __gen_page_html(self, rpath):
        editlink = """
<hr />
<p>
<a href=".edit.{name}">Edit</a>
<a href=".hist.{name}">History</a>
|
<a href=".list">List</a>
</p>
"""
        name = path.basename(rpath)
        conv = self.get_page_html(rpath)
        # rdir = path.dirname(rpath)
        return conv + editlink.format(name=name)
        return

    def get_page_html(self, rpath):
        """Get html converted content."""
        fpath = self.gen_fullpath(rpath)
        text = self.__read_file(fpath)
        return self.__md.convert(text)

