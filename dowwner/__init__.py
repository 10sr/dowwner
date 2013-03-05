#!/usr/bin/env python3

"""dowwner - Very simple wiki program using markdown

Wiki program working without external http server.
Uses markdown for markup.
"""

import os
from socket import gethostname

from dowwner.server import start

__version__ = "0.0.1"

def main(port=2505, rootdir=os.getcwd(), daemon=None, cgi=False):
    def f():
        return start(port=port, rootdir=rootdir)

    rootdir = os.path.realpath(rootdir)
    if cgi:
        from dowwner.cgi import main
        return main(rootdir)
    elif daemon:
        from dowwner.daemon import main
        pidfile = os.path.join(rootdir,
                               ".".join((".dowwner", gethostname(), "pid")))
        logfile = os.path.join(rootdir,
                               ".".join((".dowwner", gethostname(), "log")))
        return main(daemon, pidfile, logfile, f)
    else:
        return f()
