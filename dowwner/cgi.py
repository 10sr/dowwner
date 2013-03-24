#!/usr/bin/env python3

import sys
import os
# from pprint import pprint

import cgi, cgitb

from dowwner.dowwner import Dowwner

def print_redirect(p):
    print("Location: http://{}{}".format(os.environ["SERVER_NAME"], p))
    return

def main(rootdir):
    cgitb.enable()

    try:
        path_ = os.environ["PATH_INFO"]
    except KeyError:
        print_redirect(os.environ["REQUEST_URI"] + "/")
        print()
        return

    if path_ == "/" and not os.environ["REQUEST_URI"].endswith("/"):
        print_redirect(os.environ["REQUEST_URI"] + "/")
        print()
        return

    try:
        query = os.environ["QUERY_STRING"]
        path_ = "?".join((path_, query))
    except KeyError:
        pass

    met = os.environ["REQUEST_METHOD"]


    d = Dowwner(rootdir)

    if met == "GET" or met == "HEAD":
        c = d.get(path_)
        pass
    elif met == "POST":
        form = cgi.FieldStorage(keep_blank_values=True)
        c = d.post(path_, form)

    if c.redirect_r:
        print_redirect(os.path.join(os.path.dirname(os.environ["REQUEST_URI"]),
                                    c.redirect))
        print()
        return

    print("Content-Type: text/html")
    print("", flush=True)
    if met != "HEAD":
        # print(c.content_s)
        sys.stdout.buffer.write(c.content)
        #_main(rootdir)
    return

# for debugging
def _main(rootdir):
    # print(argv)
    cgi.print_environ()
    cgi.print_environ_usage()
    cgi.print_directory()

    return
