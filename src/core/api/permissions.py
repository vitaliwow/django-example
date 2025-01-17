from apps.interactions.models import Quiz
from apps.users.models import User
from django.contrib.auth.models import AnonymousUser
from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView


class HasAccessToMaterials(BasePermission):
    def has_permission(self, request: Request, view: APIView) -> bool:
        user: User | AnonymousUser = request.user

        match request.method.lower():
            case "get":
                return True
            case _:
                return user.is_authenticated and user.is_commercial and user.has_access_to_cp

    def has_object_permission(self, request: Request, view: APIView, obj: Quiz) -> bool:
        user: User | AnonymousUser = request.user

        if request.method.lower() == "get":
            return True

        return user.is_authenticated and user.is_commercial and user.has_access_to_cp
