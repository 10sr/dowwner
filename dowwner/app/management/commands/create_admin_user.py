from argparse import ArgumentParser
import os
from typing import Dict, List

from django.contrib.auth.models import User

from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Create admin user"

    def add_arguments(self, parser: ArgumentParser) -> None:
        return

    def handle(self, *args: List[str], **kargs: Dict[str, str]) -> None:
        username = "10sr"
        password = os.environ.get("ADMIN_PASSWORD", "")
        assert password, "Aborting: ADMIN_PASSWORD is empty"

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist as e:
            user = User.objects.create_user(username)

        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        self.stdout.write(f"User {user} updated.")
        return
