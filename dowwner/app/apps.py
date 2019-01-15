from django.apps import AppConfig


class DowwnerConfig(AppConfig):
    # Full Python path to the application, e.g. 'django.contrib.admin'.
    # This attribute defines which application the configuration applies to. It must be set in all AppConfig subclasses.
    # It must be unique across a Django project.
    name = "dowwner.app"
    # Short name for the application, e.g. 'admin'
    # This attribute allows relabeling an application when two applications have conflicting labels. It defaults to the last component of name. It should be a valid Python identifier.
    # It must be unique across a Django project.
    # (For dowwner app it is also used urls.py app_name
    label = "dowwner"

    dowwner_pygments_class = "dowwner-codehilite-pygments"
