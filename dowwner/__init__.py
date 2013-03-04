#!/usr/bin/env python3

"""dowwner - Very simple wiki program using markdown

Wiki program working without external http server.
Uses markdown for markup.
"""

import os
from socket import gethostname

from dowwner.server import start
from dowwner.daemon import daemon as daemon_

__version__ = "0.0.1"

def main(port=2505, rootdir=os.getcwd(), daemon=None):
    def f():
        return start(port=port, rootdir=rootdir)

    rootdir = os.path.realpath(rootdir)
    if daemon:
        pidfile = os.path.join(rootdir,
                               ".".join((".dowwner", gethostname(), "pid")))
        logfile = os.path.join(rootdir,
                               ".".join((".dowwner", gethostname(), "log")))
        return daemon_(daemon, pidfile, logfile, f)
    else:
        return f()
