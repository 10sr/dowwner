#!/usr/bin/env python3

import os

from dowwner.server import start

def main(port=2505, rootdir=os.getcwd()):
    return start(port=port, rootdir=rootdir)
