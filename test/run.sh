#!/bin/sh
set -xe

python -V
python3 -m flake8 "`dirname "$0"`"/../dowwner
