from django.contrib.auth import get_user_model
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .viewsets import UserViewSet

app_name = "users"

router = DefaultRouter()
router.register("users", UserViewSet, basename="users")

User = get_user_model()

urlpatterns = [
    path("", include(router.urls)),
]
