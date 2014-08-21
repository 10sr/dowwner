#!/usr/bin/env python3


class BaseStorage():
    """Storage base class."""

    def __init__(self, storage_name):
        """Initialize Storage."""
        raise NotImplementedError

    def isdir(self, pathstr):
        "Return True if directory named pathstr exists."
        raise NotImplementedError

    def listdir(self, pathstr):
        """Return list of files in pathstr. When dir not found, return []."""
        raise NotImplementedError

    def load(self, patht, dtype=None):
        """Load page.

        Args:
            patht: Tuple of path like (dir, base).
            dtype: String of type of data. Currently possible values are None,
                "style", "cache", "extraheader".

        Returns:
            String of content.

        Raises:
             dowwner.exc.PageNotFoundError
             dowwner.exc.NotADirectoryError
        """
        raise NotImplementedError

    def save(self, patht, data, dtype=None):
        """Save page with data.

        Args:
            patht: Tuple of path like (dir, base).
            data: String of data.
            dtype: String of type of data.
        """
        raise NotImplementedError

    def rm(self, patht, dtype=None):
        """Remove page.

        Raises:
            dowwner.exc.PageNotFoundError
        """
        raise NotImplementedError

    def getmtime(self, patht, dtype=None):
        """Get last modified time of patht.

        Returns:
            Time representing mtime of patht in the same format as time.time()
            returns. If page does not exists, raise PageNotFoundError. If the
            time is not available for another reason, return None.

        Raises:
            dowwner.exc.PageNotFoundError
        """
        raise NotImplementedError

    # methods for history handling

    def lshist(self, patht):
        """Return list of history files.

        Returns:
            If path_ indicates directory, returns the list of names of backups
            of all files in that directory. Otherwise, returns those of the
            file of patht.
            Values returned are used to load backup file with self.load_bak().
        """
        raise NotImplementedError

    def load_bak(self, patht):
        """Load backed up file.

        Basename of path_ is decided by the return of self.lshist().

        Returns:
            String of content of patht.

        Raises:
            dowwner.exc.PageNameError
        """
        raise NotImplementedError

    # methods for archiving

    def zip(self, pathstr):
        """Create zip archive for dir pathstr and return archive file as bytes.
        """
        raise NotImplementedError

    def search(self, words, pathstr, listall=False):
        """Search words from pathstr.

        Args:
            words: Iterable of word to search
            pathstr: String of path to search for words
            listall: False to list only first matched line for each file

        Returns:
            Iterable of iterable like (pathstr, matched_line) .
        """
        raise NotImplementedError

    # methods for cache

    # def save_cache(self, path_, data):
    #     """Save data as cache of path_."""
    #     raise NotImplementedError

    # def load_cache(self, path_):
    #     """Load cache of path_.

    #     Returns:
    #         String of cache saved by save_cache() or None if cache not found
    #         or is old.

    #     Raises:
    #         dowwner.exc.PageNotFoundError: Original page for Path_ not found
    #     """
    #     raise NotImplementedError

    # # methods for header

    # def save_extra_tags(self, path_, data):
    #     """Save extra tags.

    #     Save extra tags for the directory of path_.
    #     Can be read by self.load_extra_tags() .

    #     Args:
    #         path_: Path object. Always treated as directory.
    #         data: String of tags.
    #     """
    #     raise NotImplementedError

    # def load_extra_tags(self, path_):
    #     """Load extra tags.

    #     Load extra tags saved by self.save_extra_tags() .

    #     Returns:
    #         String of data saved by self.save_extra_tags() or None if not
    #         found.
    #     """
    #     raise NotImplementedError

if __name__ == "__main__":
    pass
