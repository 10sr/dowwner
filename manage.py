#!/usr/bin/env python3
import os
from pathlib import Path
import sys
from typing import List

from django.core.management import execute_from_command_line


def main(argv: List[str]) -> int:
    # TODO: How to check if going to run tests?
    if os.environ["DOWWNER_ENV"] == "test":
        os.environ["DJANGO_SETTINGS_MODULE"] = "tests.settings"
    else:
        os.environ.setdefault("DOWWNER_ENV", "local")
        os.environ[
            "DJANGO_SETTINGS_MODULE"
        ] = f"dowwner.settings_{os.environ['DOWWNER_ENV']}"

    execute_from_command_line(argv)
    return 0


# TODO: Use django-admin and remove this file?
if __name__ == "__main__":
    sys.exit(main(sys.argv))
