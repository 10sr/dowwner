from django.shortcuts import render

from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.utils.safestring import mark_safe

from . import models

from . import markdown

# Create your views here.


def index(request: HttpRequest) -> HttpResponse:
    return HttpResponse(
        f"""index
        <a href="v/test/page">test/page</a>
        <a href="v/test2">test2</a>
        <a href="admin">admin</a>
        <p>{dir(request)}</p>
        """
    )


def v(request: HttpRequest, path_: str = "") -> HttpResponse:
    try:
        p = models.Page.objects.get(path=path_)
    except models.Page.DoesNotExist as e:
        # TODO: Redirect to edit page
        return HttpResponse(f"Not found: {path_}")
    html = markdown.to_html(p.markdown)

    editurl: str
    if path_ == "":
        editurl = reverse("dowwner:e_root")
    else:
        editurl = reverse("dowwner:e", args=[path_])

    template = loader.get_template("dowwner/v.html.dtl")
    return HttpResponse(
        template.render(
            {
                "content": mark_safe(html),
                "pagename": path_,
                # TODO: OK to generate in template file?
                "edit_page": editurl,
            }
        )
    )


def e(request: HttpRequest, path_: str = "") -> HttpResponse:
    try:
        p = models.Page.objects.get(path=path_)
    except models.Page.DoesNotExist as e:
        # TODO: Open as empty
        return HttpResponse(f"Not found: {path_}")

    template = loader.get_template("dowwner/e.html.dtl")
    return HttpResponse(template.render({"raw": p.markdown}))
