from django.shortcuts import render
from django.db import connections
from django.http import JsonResponse
from rest_framework import status

def live(request):
    return JsonResponse({"status": "ok"}, headers={"Cache-Control": "no-store"})

def ready(request):
    try:
        with connections["default"].cursor() as cursor:
            cursor.execute("SELECT 1;")
    except Exception as e:
        return JsonResponse({"status": "fail", "error": str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE, headers={"Cache-Control": "no-store"})
    return JsonResponse({"status": "ok"}, headers={"Cache-Control": "no-store"})