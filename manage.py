#!/usr/bin/env python3
import os
import sys
from pathlib import Path


# TODO: How to check if going to run tests?
if sys.argv[1] == "test":
    os.environ["DOWWNER_ENV"] = "test"
    os.environ["DJANGO_SETTINGS_MODULE"] = "tests.settings"
else:
    os.environ.setdefault("DOWWNER_ENV", "local")
    os.environ["DJANGO_SETTINGS_MODULE"] = f"dowwner.settings_{os.environ['DOWWNER_ENV']}"

os.environ["DOWWNER_BASE_DIR"] = str(Path(__file__).resolve().parent)

from django.core.management import execute_from_command_line

execute_from_command_line(sys.argv)
