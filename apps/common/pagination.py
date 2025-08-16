from rest_framework.pagination import LimitOffsetPagination
from urllib.parse import urlsplit
from rest_framework.response import Response

class CustomLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 20
    max_limit = 50

    def _to_relative(self, url: str | None) -> str | None:
        """
        Convert absolute URL to relative URL
        """
        if not url:
            return None
        parts = urlsplit(url)
        return parts.path + (f"?{parts.query}" if parts.query else "")

    def get_paginated_response(self, data):
        return Response({
            'count': self.count,
            'next': self._to_relative(self.get_next_link()),
            'previous': self._to_relative(self.get_previous_link()),
            'results': data
        })