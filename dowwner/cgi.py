#!/usr/bin/env python3

import sys
import os
# from pprint import pprint

import cgi

from dowwner import exc

def print_redirect(p):
    print("Location: http://{}{}{}".format(os.environ["SERVER_NAME"],
                                           os.environ["SCRIPT_NAME"],
                                           p))
    return

def main(rootdir, tb=True):
    if tb:
        import cgitb
        cgitb.enable()

    try:
        pathstr = os.environ["PATH_INFO"]
    except KeyError:
        print_redirect("/")
        print()
        return

    if pathstr == "": # and not os.environ["REQUEST_URI"].endswith("/"):
        # this is not good because REQUEST_URI is not assured to exist,
        print_redirect("/")
        print()
        return

    try:
        query = os.environ["QUERY_STRING"]
    except KeyError:
        query = ""

    met = os.environ["REQUEST_METHOD"]

    from dowwner.dowwner import Dowwner
    d = Dowwner(rootdir)

    if met == "GET" or met == "HEAD":
        c = d.req_http("get", pathstr, query)
    elif met == "POST":
        form = cgi.FieldStorage(keep_blank_values=True)
        c = d.req_http("post", pathstr, query, form)

    status = c[0]
    message = c[1]
    redirect = c[2]
    headers = c[3]
    content = c[4]

    print("Status: {} {}".format(status, message))

    for k, v in headers.items():
        print("{}: {}".format(k, v))
    if redirect:
        print_redirect(os.path.join(os.path.dirname(pathstr),
                                    redirect))
    print("", flush=True)

    if met.lower() != "head":
        sys.stdout.buffer.write(content)
        #_debug()
    return

def _debug():
    print("Status: 200 OK")
    print("Content-Type: text/html")
    print()
    cgi.print_environ()
    cgi.print_environ_usage()
    cgi.print_directory()
    return
