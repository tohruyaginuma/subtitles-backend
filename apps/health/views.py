from django.shortcuts import render
from django.db import connections

from apps.common.responses import ok

# Create your views here.
def live(request):
    return ok({"status": "ok"})