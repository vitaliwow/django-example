from django.conf import settings
from django.contrib import admin
from django.urls import URLPattern, URLResolver, include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


URL = URLPattern | URLResolver
URLList = list[URL]

api: URLList = [
    path("v1/docs/", SpectacularAPIView.as_view(), name="schema"),
    path("v1/docs/swagger-ui/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("v1/docs/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path("", include("apps.a12n.urls", namespace="auth")),
    path("", include("apps.choices.urls", namespace="choices")),
    path("", include("apps.interactions.urls", namespace="interactions")),
    path("", include("apps.playlists.urls", namespace="playlists")),
    path("", include("apps.suggestions.urls", namespace="suggestions")),
    path("", include("apps.summarization.urls", namespace="summarization")),
    path("", include("apps.videos.urls", namespace="videos")),
    path("", include("apps.users.urls", namespace="users")),
]

urlpatterns = [
    path("api/", include(api)),
    path("admin/", admin.site.urls),
]
