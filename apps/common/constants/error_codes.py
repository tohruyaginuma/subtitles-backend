from rest_framework.exceptions import (
    ValidationError, NotAuthenticated, AuthenticationFailed,
    PermissionDenied, NotFound, Throttled
)
from rest_framework import status
from django.http import Http404

ERROR_CODE = {
    ValidationError:      ("validation_error", status.HTTP_400_BAD_REQUEST), 
    NotAuthenticated:     ("not_authenticated", status.HTTP_401_UNAUTHORIZED),
    AuthenticationFailed: ("invalid_credentials", status.HTTP_401_UNAUTHORIZED),
    PermissionDenied:     ("permission_denied", status.HTTP_403_FORBIDDEN),
    NotFound:             ("not_found", status.HTTP_404_NOT_FOUND),
    Http404:              ("not_found", status.HTTP_404_NOT_FOUND),
    Throttled:            ("rate_limited", status.HTTP_429_TOO_MANY_REQUESTS),
    Exception:            ("error", status.HTTP_500_INTERNAL_SERVER_ERROR),
}