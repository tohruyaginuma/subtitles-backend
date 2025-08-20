from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.response import Response
from .constants.error_codes import ERROR_CODE
from rest_framework import status
from django.conf import settings
import traceback

def exception_handler(exc, context):
    response = drf_exception_handler(exc, context)

    if response is not None:
        details = response.data
        flat_msg = None
        if isinstance(details, dict):
            first_value = next(iter(details.values()))
            if isinstance(first_value, list):
                flat_msg = "; ".join(str(v) for v in first_value)
            else:
                flat_msg = str(first_value)
        else:
            flat_msg = str(details)

        response.data = {
            "error": {
                "code": ERROR_CODE.get(type(exc), ("error", response.status_code))[0],
                "message": flat_msg,
                "details": details
            }
        }
    else:
        error_code, status_code = ERROR_CODE.get(
            Exception, ("server_error", status.HTTP_500_INTERNAL_SERVER_ERROR)
        )

        response = Response({
            "error": {
                "code": error_code,
                "message": str(exc) if settings.DEBUG else "Internal server error",
                "details":  traceback.format_exc() if settings.DEBUG else None
            }
        }, status=status_code)

    return response