from django.urls import include, path

app_name = "playlists"

urlpatterns = [
    path("v1/", include("apps.playlists.api.v1.urls")),
]
