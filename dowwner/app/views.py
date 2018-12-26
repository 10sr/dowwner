from django.shortcuts import render

from django.http import HttpResponse

from . import models

# Create your views here.


def index(request):
    return HttpResponse(f"index {dir(request)}")
