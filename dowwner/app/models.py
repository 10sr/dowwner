from django.db import models

# Create your models here.


class Page(models.Model):
    created_at = models.DateTimeField("date created")
    updated_at = models.DateTimeField("date updated")
    # content is better?
    markdown = models.TextField(max_length=5000, default="")
    # Empty value for path is allowed, which means the "root" page
    path = models.CharField(max_length=200, unique=True)
    # TODO: Add relation to created user and updated user
