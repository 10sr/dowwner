import inspect

from django.contrib import admin
from django.db.models import Model

from . import models
from .apps import DowwnerConfig


# Configure site header
admin.AdminSite.site_header = "Dowwner Admin"

# Register all models to admin page
# https://docs.djangoproject.com/en/1.10/intro/tutorial02/#make-the-poll-app-modifiable-in-the-admin
# TODO: Use Appconfig.get_modoels()
for key in dir(models):
    e = getattr(models, key)
    if inspect.isclass(e) and issubclass(e, Model):
        admin.site.register(e)
