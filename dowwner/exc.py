#!/usr/bin/env python3

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
    def __init__(self, url):
        self.url = url
        return

class PermanentRedirection(Redirection):
    pass

class SeeOtherRedirection(Redirection):
    pass
