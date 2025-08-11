from django.shortcuts import render
from django.db import connections
from django.http import JsonResponse

# Create your views here.
def live(request):
    resp = JsonResponse({"status": "ok"})
    resp["Cache-Control"] = "no-store"
    return resp