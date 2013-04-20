#!/usr/bin/env python3

"""dowwner - Very simple markdown wiki clone

Uses Markdown for markup and pages are stored as plain markdown files.
Works both as a cgi program and as a server.
"""

from __future__ import absolute_import

import os
# import locale

__version__ = "0.4.3"

def main(port=2505, rootdir=os.getcwd(), daemon=None, cgi=False):
    def f():
        from dowwner.server import Server
        s = Server(port=port, rootdir=rootdir)
        return s.start()

    rootdir = os.path.realpath(rootdir)
    # locale.setlocale(locale.LC_ALL, "ja_JP.UTF-8")

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

        import dowwner.daemon

        if daemon == "start":
            return dowwner.daemon.start(pidfile, logfile, f)
        elif daemon == "restart":
            return dowwner.daemon.restart(pidfile, logfile, f)
        elif daemon == "status":
            return dowwner.daemon.status(pidfile)
        elif daemon == "stop":
            return dowwner.daemon.stop(pidfile)

    else:
        return f()
