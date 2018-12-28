from argparse import ArgumentParser
import os
from typing import Dict, List

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from dowwner.app import models


class Command(BaseCommand):
    help = "Add a test pages"

    def add_arguments(self, parser: ArgumentParser) -> None:
        return

    def _addrecord(self, path_: str, markdown: str) -> None:
        try:
            p = models.Page.objects.get(path=path_)
        except models.Page.DoesNotExist as e:
            self.stdout.write("Page {} not exists, creating".format(path_))
            now = timezone.now()
            models.Page(
                path=path_, markdown=markdown, created_at=now, updated_at=now
            ).save()
            return

        self.stdout.write("Page `{}' already exists, ignoring".format(path_))
        # p.markdown = markdown
        # p.save()
        return

    def handle(self, *args: List[str], **kargs: Dict[str, str]) -> None:
        self._addrecord(
            "test/page",
            "**test page** [[wikilinktest]] [[spaced link]] [[link/with/slashes]]",
        )
        self._addrecord("", "This is root page [[hoe]]")
        self._addrecord("hoe", "hoehoehoe")
        return
