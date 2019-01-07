# from django.conf.urls import include, url
from django.urls import include, path, re_path
from . import views
from django.views.generic.base import RedirectView

app_name = "dowwner"
urlpatterns = [
    path("", views.index, name="index"),
    # TODO: These URL are temporal
    # Use regexp to allow slashes in path_
    re_path(r"v/(?P<path_>[_0-9a-zA-Z/]+)", views.v, name="v"),
    path("v", RedirectView.as_view(url="v/"), name="v_root_redirect"),
    path("v/", views.v, name="v_root"),
    re_path(r"e/(?P<path_>[_0-9a-zA-Z/]+)", views.e, name="e"),
    # path("e", RedirectView.as_view(url="e/"), name="e_root_redirect"),
    path("e/", views.e, name="e_root"),
]
