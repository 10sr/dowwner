#!/usr/bin/env python3

class DowwnerException(Exception):
    pass


class PageNameError(DowwnerException):
    short = "Invalid page name"

class PageNotFoundError(PageNameError):
    short = "Page not found"

class NotADirectoryError(PageNameError):
    short = "Directory not found"

class OperatorError(PageNameError):
    short = "Invalid operator"


class Redirection(DowwnerException):
    def __init__(self, url):
        self.url = url
        return

class PermanentRedirection(Redirection):
    pass

class SeeOtherRedirection(Redirection):
    pass
