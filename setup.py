#!/usr/bin/env python3

from distutils.core import setup

import dowwner

setup(name = "dowwner",
      version = dowwner.__version__,
      description = "Very simple wiki program using markdown",
      long_description = dowwner.__doc__,
      author = "10sr",
      author_email = "sr10@sourceforge.org",
      url = "https://10sr.github.com/dowwner",
      download_url = "https://github.com/10sr/dowwner/archive/master.zip",
      packages = ["dowwner", "dowwner/markdown"],
      scripts = ["bin/dowwner"],
      keywords = "wiki",
      classifiers=['License :: Public Domain']
      )
