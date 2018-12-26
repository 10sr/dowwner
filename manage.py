#!/usr/bin/env python3
import os
import sys
from pathlib import Path
from typing import List

from django.core.management import execute_from_command_line


def main(argv: List[str]) -> int:
    # TODO: How to check if going to run tests?
    if argv[1] == "test":
        os.environ["DOWWNER_ENV"] = "test"
        os.environ["DJANGO_SETTINGS_MODULE"] = "tests.settings"
    else:
        os.environ.setdefault("DOWWNER_ENV", "local")
        os.environ[
            "DJANGO_SETTINGS_MODULE"
        ] = f"dowwner.settings_{os.environ['DOWWNER_ENV']}"

    os.environ["DOWWNER_BASE_DIR"] = str(Path(__file__).resolve().parent)

    execute_from_command_line(sys.argv)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
