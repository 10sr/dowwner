#!/usr/bin/env python3

class PageNameError(ValueError):
    pass

class PageNotFoundError(PageNameError):
    pass

class DirNotFoundError(PageNameError):
    pass

class OperatorError(PageNameError):
    pass
