from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.response import Response
from .constants.error_codes import ERROR_CODE

def exception_handler(exc, context):
    response = drf_exception_handler(exc, context)

    if response is not None:
        details = response.data
        flat_msg = None
        if isinstance(details, dict):
            first_value = next(iter(details.values()))
            if isinstance(first_value, list) and first_value:
                flat_msg = str(first_value[0])
            else:
                flat_msg = str(first_value)
        else:
            flat_msg = str(details)

        response.data = {
            "data": None,
            "error": {
                "code": ERROR_CODE.get(type(exc), ("error", response.status_code))[0],
                "message": flat_msg,
                "details": details
            }
        }
    else:
        response = Response({
            "data": None,
            "error": {
                "code": "server_error",
                "message": str(exc),
                "details": None
            }
        }, status=500)

    return response