from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        error_detail = response.data
        response.data = {
            "data": None,
            "error": error_detail  # you can flatten this if needed
        }

    return response