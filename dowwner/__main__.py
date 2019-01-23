import os
import sys
from typing import List

import click


@click.group()
def cli() -> None:
    # Manually setup django environment
    # https://docs.djangoproject.com/en/2.1/topics/settings/
    os.environ.setdefault("DOWWNER_ENV", "local")
    os.environ[
        "DJANGO_SETTINGS_MODULE"
    ] = f"dowwner.settings_{os.environ['DOWWNER_ENV']}"

    import django

    django.setup()
    return


@cli.command()
@click.argument("name")
def add_admin_user(name: str) -> None:
    from django.contrib.auth.models import User
    from django.core.management.base import BaseCommand, CommandError

    password = os.environ.get("ADMIN_PASSWORD", "")
    assert password, "Aborting: ADMIN_PASSWORD is empty"

    user: User
    try:
        user = User.objects.get(username=name)
    except User.DoesNotExist as e:
        user = User.objects.create_user(name)

    user.set_password(password)
    user.is_superuser = True
    user.is_staff = True
    user.save()
    print(f"User {user} updated.")
    return


if __name__ == "__main__":
    cli()
