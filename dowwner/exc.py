#!/usr/bin/env python3

from urllib.parse import quote

class DowwnerBaseException(BaseException):
    pass

class DowwnerException(DowwnerBaseException):
    pass


class PageNameError(DowwnerException):
    short = "Invalid page name"

class PageNotFoundError(PageNameError):
    short = "Page not found"

class NotADirectoryError(PageNameError):
    short = "Directory not found"

class OperatorError(PageNameError):
    short = "Invalid operator"


class PageNotModified(DowwnerBaseException):
    pass


class Redirection(DowwnerBaseException):
    status = 300
    def __init__(self, url):
        self.url = quote(url, encoding="utf-8")
        return

    str_base = "Page redirected to {}"
    def __str__(self):
        return self.str_base.format(self.url)

class PermanentRedirection(Redirection):
    status = 301
    short = "Moved parmanently"
    str_base = "page moved parmanently to {}"

class SeeOtherRedirection(Redirection):
    status = 303
    short = "See other"
    str_base = "See {}"
