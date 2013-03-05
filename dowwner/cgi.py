#!/usr/bin/env python3

import sys
import os
from pprint import pprint

import cgi, cgitb

def main(rootdir):
    cgitb.enable()

    print("Content-Type: text/html")
    print()

    form = cgi.FieldStorage()

    print(__name__)
    print("cgi")
    # print(argv)
    print(rootdir)
    print(form)
    cgi.print_environ()
    cgi.print_environ_usage()
    cgi.print_directory()

    try:
        path_ = os.environ["PATH_INFO"]
    except KeyError:
        path_ = "/"
    print("<p>")
    print(path_)
    print("</p>")

    return
