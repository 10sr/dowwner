#!/usr/bin/env python3

"""dowwner - Very simple wiki program using markdown

Wiki program working without external http server.
Uses markdown for markup.
"""

import os

from dowwner.server import start

__version__ = "0.0.1"

def main(port=2505, rootdir=os.getcwd()):
    return start(port=port, rootdir=rootdir)
