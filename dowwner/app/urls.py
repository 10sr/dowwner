from django.conf.urls import include, url
from . import views

# TODO: Is this correct?
app_name = "dowwner"
urlpatterns = [
    url(r"^$", views.index, name="index"),
    # TODO: Ths URL is temporal
    # Use regexp to allow slashes in path_
    url(r"v/(?P<path_>[_0-9a-zA-Z/]+)", views.v, name="v"),
]
