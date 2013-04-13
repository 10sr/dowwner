#!/usr/bin/env python3

# todo: add exception for redirect

class PageNameError(ValueError):
    short = "Invalid page name"
    pass

class PageNotFoundError(PageNameError):
    short = "Page not found"
    pass

class NotADirectoryError(PageNameError):
    short = "Directory not found"
    pass

class OperatorError(PageNameError):
    short = "Invalid operator"
    pass
