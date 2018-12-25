from django.conf.urls import include, url
from dowwner.app import views

app_name = "dowwner"
urlpatterns = [
    url(r"^$", views.index, name="index"),
]
