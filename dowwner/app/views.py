from django.shortcuts import render

from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseRedirect,
    HttpResponseBadRequest,
)
from django.template import loader
import django.urls
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.views.decorators.http import etag

from typing import Iterable

from . import models
from .apps import DowwnerConfig

from . import markdown
from . import pygments


def _reverse(name: str, args: Iterable[str] = ()) -> str:
    r = django.urls.reverse(f"{DowwnerConfig.label}:{name}", args=args)
    assert isinstance(r, str)
    return r


def index(request: HttpRequest) -> HttpResponse:
    return HttpResponse(
        f"""index
        <a href="v/test/page">test/page</a>
        <a href="v/hoe">hoe</a>
        <a href="admin">admin</a>
        <p>{dir(request)}</p>
        """
    )


def v(request: HttpRequest, path_: str = "") -> HttpResponse:
    editurl: str
    if path_ == "":
        editurl = _reverse("e_root")
    else:
        editurl = _reverse("e", args=[path_])

    try:
        p = models.Page.objects.get(path=path_)
    except models.Page.DoesNotExist as e:
        # TODO: Redirect to edit page
        return HttpResponse(
            f"""Not found: {path_}
        <a href="{editurl}">Create new</a>"""
        )
    html = markdown.to_html(p.markdown)

    template = loader.get_template("dowwner/v.html.dtl")
    return HttpResponse(
        template.render(
            {
                "content": mark_safe(html),
                "pagename": path_,
                # TODO: OK to generate in template file?
                "edit_page": editurl,
                "pygments_css": _reverse("pygments_css", args=["default"]),
            }
        )
    )


def e(request: HttpRequest, path_: str = "") -> HttpResponse:
    content: str
    try:
        p = models.Page.objects.get(path=path_)
        content = p.markdown
    except models.Page.DoesNotExist as e:
        # TODO: Add alert that page does not exist
        content = ""

    post_page_path: str
    if path_ == "":
        post_page_path = _reverse("post_page_root")
    else:
        post_page_path = _reverse("post_page", args=[path_])

    template = loader.get_template("dowwner/e.html.dtl")
    return HttpResponse(
        template.render(
            {"raw": content, "post_page_path": post_page_path},
            # Requred for csrf_token
            request,
        )
    )


def post_page(request: HttpRequest, path_: str = "") -> HttpResponse:
    try:
        content = request.POST["content"]
    except KeyError:
        # TODO: How to handle this?
        return HttpResponseBadRequest("content not given")

    now = timezone.now()
    p: models.Page
    try:
        # TODO: Add history for model
        p = models.Page.objects.get(path=path_)
        p.markdown = content
        p.update_at = now
    except models.Page.DoesNotExist as e:
        p = models.Page(path=path_, markdown=content, created_at=now, updated_at=now)
    p.save()

    v: str
    if path_ == "":
        v = _reverse("v_root")
    else:
        v = _reverse("v", args=[path_])
    return HttpResponseRedirect(v)


def _etag_pygments_css(request: HttpRequest, style: str) -> str:
    return f"PYGMENTS_CSS_{pygments.pygments_version}_{style}"


@etag(_etag_pygments_css)
def pygments_css(request: HttpRequest, style: str) -> HttpResponse:
    return HttpResponse(pygments.get_css(style), content_type="text/css")
