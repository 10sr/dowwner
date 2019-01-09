from django.shortcuts import render

from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseRedirect,
    HttpResponseBadRequest,
)
from django.template import loader
from django.urls import reverse
from django.utils import timezone
from django.utils.safestring import mark_safe

from . import models
from .apps import DowwnerConfig

from . import markdown

_app_name = DowwnerConfig.label

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
        editurl = reverse(f"{_app_name}:e_root")
    else:
        editurl = reverse(f"{_app_name}:e", args=[path_])

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

    post_page_path: str
    if path_ == "":
        post_page_path = reverse(f"{_app_name}:post_page_root")
    else:
        post_page_path = reverse(f"{_app_name}:post_page", args=[path_])

    template = loader.get_template("dowwner/e.html.dtl")
    return HttpResponse(
        template.render(
            {"raw": p.markdown, "post_page_path": post_page_path},
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
        v = reverse(f"{_app_name}:v_root")
    else:
        v = reverse(f"{_app_name}:v", args=[path_])
    return HttpResponseRedirect(v)
