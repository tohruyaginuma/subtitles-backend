from rest_framework.exceptions import (
    ValidationError, NotAuthenticated, AuthenticationFailed,
    PermissionDenied, NotFound, Throttled
)

from django.http import Http404

ERROR_CODE = {
    ValidationError:      ("validation_error", 400), 
    NotAuthenticated:     ("not_authenticated", 401),
    AuthenticationFailed: ("invalid_credentials", 401),
    PermissionDenied:     ("permission_denied", 403),
    NotFound:             ("not_found", 404),
    Http404:              ("not_found", 404),
    Throttled:            ("rate_limited", 429),
}   