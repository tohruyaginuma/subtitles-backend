from rest_framework.response import Response

def ok(data, status=200, **extra):
    payload = {"data": data, "error": None}
    if extra:
        payload.update(extra)
    return Response(payload, status=status)

def created(data):
    return ok(data, status=201)

def no_content():
    return Response(status=204)