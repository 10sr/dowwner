"""dowwner URL Configuration"""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import RedirectView


urlpatterns = [
    path("dowwner/admin/", admin.site.urls),
    # url(r"^login$", auth_views.login, name="login"),
    # Following names are imported from django.contrib.auth.urls
    # - login
    # - logout
    # - password_change
    # - password_reset
    # - password_reset_done
    # - password_reset_confirm
    # - password_reset_complete
    path("dowwenr/", include("django.contrib.auth.urls")),
    path("dowwner/", include("dowwner.app.urls")),
    path("", RedirectView.as_view(url="dowwner/")),
]
