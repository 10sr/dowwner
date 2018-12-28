from django.shortcuts import render

from django.http import HttpRequest, HttpResponse
from django.template import loader
from django.utils.safestring import mark_safe

from . import models

from . import markdown

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
        # TODO: Redirect to edit page
        return HttpResponse(f"Not found: {path_}")
    html = markdown.to_html(p.markdown)

    template = loader.get_template("dowwner/v.html.dtl")
    return HttpResponse(template.render({"content": mark_safe(html)}))
