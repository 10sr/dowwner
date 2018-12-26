from argparse import ArgumentParser
import os
from typing import Dict, List

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from dowwner.app import models


class Command(BaseCommand):
    help = "Add a test page"

    __path = "test/page"
    __markdown = "**test page**"

    def add_arguments(self, parser: ArgumentParser) -> None:
        return

    def handle(self, *args: List[str], **kargs: Dict[str, str]) -> None:
        try:
            p = models.Page.objects.get(path=self.__path)
            self.stdout.write("Page `{}' already exists".format(self.__path))
        except models.Page.DoesNotExist as e:
            self.stdout.write("Page {} not exists, creating".format(self.__path))
            now = timezone.now()
            models.Page(
                path=self.__path,
                markdown=self.__markdown,
                created_at=now,
                updated_at=now,
            ).save()
        return
