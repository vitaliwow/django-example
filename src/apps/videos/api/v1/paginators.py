from collections import OrderedDict

from django.db.models import QuerySet
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.request import Request
from rest_framework.response import Response


class VideoSearchPagination(LimitOffsetPagination):
    def paginate_queryset(self, queryset: QuerySet, request: Request, view=None) -> list | None:  # noqa:ANN001
        self.limit = self.get_limit(request)
        if self.limit is None:
            return None
        self.offset = self.get_offset(request)
        self.request = request
        self.count = len(queryset)
        if self.count > self.limit and self.template is not None:
            self.display_page_controls = True
        if self.count == 0 or self.offset > self.count:
            return []
        return list(queryset[self.offset : self.offset + self.limit])

    def get_paginated_response(self, data: list[dict]) -> Response:
        return Response(
            OrderedDict(
                [
                    ("count", self.count),
                    ("next", self.get_next_link()),
                    ("previous", self.get_previous_link()),
                    ("results", data),
                ],
            ),
        )
