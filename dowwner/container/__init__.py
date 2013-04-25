#!/usr/bin/env python3

class BaseContainer():
    """Container base class."""
    def __init__(self):
        """Initialize Container."""
        raise NotImplementedError

    def isdir(self, path_):
        "Return True if directory named path exists."
        raise NotImplementedError

    def listdir(self, path_):
        """Return list of files in path_. When dir not found, return []."""
        raise NotImplementedError

    def load(self, path_, raw=False):
        """Load page.

        If path_.isstyle == True, always return raw contents of path_,
        otherwise return contents as html if raw == False.
        If path_.path ends with slash, try to load "index" page.

        Args:
            path_: Path object.
            raw: False to convert contents to html.

        Returns:
            String of content.

        Raises:
             dowwner.exc.PageNotFoundError
             dowwner.exc.NotADirectoryError
        """
        raise NotImplementedError

    def save(self, path_, data):
        """Save page with data.

        Args:
            path_: Path object.
            data: String of data.
        """
        raise NotImplementedError

    def rm(self, path_):
        """Remove page.

        Raises:
            dowwner.exc.PageNotFoundError
        """
        raise NotImplementedError

    def getmtime(self, path_):
        """Get last modified time of path_.

        Returns:
            Time representing mtime of path_ in the same format as time.time()
            returns. If page does not exists, raise PageNotFoundError. If the
            time is not available for another reason, return None.

        Raises:
            dowwner.exc.PageNotFoundError
        """
        raise NotImplementedError

    # methods for history handling

    def lshist(self, path_):
        """Return list of history files.

        Returns:
            If path_ indicates directory, returns the list of names of backups
            of all files in that directory. Otherwise, returns those of the
            file of path_.
            Values returned are used to load backup file with self.load_bak().
        """
        raise NotImplementedError

    def load_bak(self, path_, raw=False):
        """Load backed up file.

        Basename of path_ is decided by the return of self.lshist().

        Returns:
            String of content of path_, as html if raw == True.

        Raises:
            dowwner.exc.PageNameError
        """
        raise NotImplementedError

    # functions for archiving

    def zip(self, path_):
        """Create zip archive for dir path_ and return archive file as bytes."""
        raise NotImplementedError

    # functions for cache

    def save_cache(self, path_, data):
        """Save data as cache of path_."""
        raise NotImplementedError

    def load_cache(self, path_):
        """Load cache of path_.

        Returns:
            String of cache saved by save_cache() or None if cache not found
            or is old.

        Raises:
            dowwner.exc.PageNotFoundError: Original page for Path_ not found
        """
        raise NotImplementedError

if __name__ == "__main__":
    pass
