"""dowwner URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse


def _redirect_root(request: HttpRequest) -> HttpResponse:
    return HttpResponseRedirect("dowwner/")


urlpatterns = [
    url(r"^dowwner/admin/", admin.site.urls),
    # url(r"^login$", auth_views.login, name="login"),
    # Following names are imported from django.contrib.auth.urls
    # - login
    # - logout
    # - password_change
    # - password_reset
    # - password_reset_done
    # - password_reset_confirm
    # - password_reset_complete
    url(r"^dowwenr/", include("django.contrib.auth.urls")),
    url(r"^dowwner/", include("dowwner.app.urls")),
    url(r"^$", _redirect_root),
]
