from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.views import APIView


class SpecialUserPermission(IsAuthenticated):
    """Add constraints"""

    def has_permission(self, request: Request, view: APIView) -> bool:
        return bool(
            request.user and request.user.is_authenticated and (request.user.is_commercial or request.user.is_staff),
        )
