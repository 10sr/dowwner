from django.shortcuts import render

from django.http import HttpRequest, HttpResponse

from . import models

# Create your views here.


def index(request: HttpRequest) -> HttpResponse:
    return HttpResponse(
        f"""index
        <a href="v/test/page">test/page</a>
        <a href="admin">admin</a>
        <p>{dir(request)}</p>
        """
    )


def v(request: HttpRequest, path_: str) -> HttpResponse:
    try:
        p = models.Page.objects.get(path=path_)
    except models.Page.DoesNotExist as e:
        return HttpResponse(f"Not found: {path_}")
    return HttpResponse(f"Content: {p.markdown}")
