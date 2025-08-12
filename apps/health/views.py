from django.shortcuts import render
from django.db import connections
from django.http import JsonResponse

# Create your views here.
def live(request):
    return JsonResponse({"status": "ok"}, headers={"Cache-Control": "no-store"})

def ready(request):
    try:
        # Simple DB check
        with connections["default"].cursor() as cursor:
            cursor.execute("SELECT 1;")
    except Exception as e:
        return JsonResponse({"status": "fail", "error": str(e), "kind": "readiness"}, status=503, headers={"Cache-Control": "no-store"})
    return JsonResponse({"status": "ok", "kind": "readiness"}, headers={"Cache-Control": "no-store"})