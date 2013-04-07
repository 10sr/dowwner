#!/usr/bin/env python3

# todo: add exception for redirect

class PageNameError(ValueError):
    pass

class PageNotFoundError(PageNameError):
    pass

class DirNotFoundError(PageNameError):
    pass

class OperatorError(PageNameError):
    pass
