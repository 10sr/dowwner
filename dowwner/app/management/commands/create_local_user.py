from argparse import ArgumentParser
import os
from typing import Dict, List

from django.contrib.auth.models import User

from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Create local user"

    def add_arguments(self, parser: ArgumentParser) -> None:
        return

    def handle(self, *args: List[str], **kargs: Dict[str, str]) -> None:
        assert (
            os.environ["NERU_ENV"] == "local"
        ), "Do not use this command in production"
        username = "user"
        password = "pw"

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist as e:
            user = User.objects.create_user(username)

        user.set_password(password)
        user.save()
        return
