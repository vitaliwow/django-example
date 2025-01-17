import typing as t

from rest_framework.request import Request
from rest_framework.views import APIView

from core.conf import api


class BaseThrottle(t.Protocol):
    def allow_request(self, request: Request, view: APIView) -> bool:
        ...


class ConfigurableThrottlingMixin:
    def allow_request(self: BaseThrottle, request: Request, view: APIView) -> bool:
        if api.DISABLE_THROTTLING:
            return True

        return super().allow_request(request, view)  # type: ignore
