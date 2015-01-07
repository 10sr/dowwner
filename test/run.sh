#!/bin/sh
set -xe

python3 -m flake8 "`dirname "$0"`"/..
