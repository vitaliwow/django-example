from django.urls import include, path
from rest_framework.routers import SimpleRouter

from apps.playlists.api.v1 import views, viewsets

playlist_router = SimpleRouter()
playlist_router.register("playlists", viewsets.PlaylistViewSet)

category_router = SimpleRouter()
category_router.register("categories", viewsets.CategoryViewSet)

urlpatterns = [
    path("", include(playlist_router.urls)),
    path("", include(category_router.urls)),
    path("playlists/read/private-link/", views.PrivateLinkAPIView.as_view(), name="get-private-link"),
    path(
        "playlists/<str:playlist_pk>/create/private-link/",
        views.PrivateLinkCreateAPIView.as_view(),
        name="create-private-link",
    ),
]
