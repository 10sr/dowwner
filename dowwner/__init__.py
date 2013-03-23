#!/usr/bin/env python3

"""dowwner - Very simple wiki program using markdown

Wiki program working without external http server.
Uses markdown for markup.
"""

import os

__version__ = "0.2"

def main(port=2505, rootdir=os.getcwd(), daemon=None, cgi=False):
    def f():
        from dowwner.server import start
        return start(port=port, rootdir=rootdir)

    rootdir = os.path.realpath(rootdir)

    if cgi:
        from dowwner.cgi import main
        return main(rootdir)

    elif daemon:
        from socket import gethostname
        hostname = gethostname()
        pidfile = os.path.join(rootdir,
                               ".".join((".dowwner", hostname, "pid")))
        logfile = os.path.join(rootdir,
                               ".".join((".dowwner", hostname, "log")))

        from dowwner.daemon import main
        return main(daemon, pidfile, logfile, f)

    else:
        return f()
