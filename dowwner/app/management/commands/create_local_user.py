import os

from django.contrib.auth.models import User

from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Create local user"

    def add_arguments(self, parser):
        return

    def handle(self, *args, **kargs):
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
