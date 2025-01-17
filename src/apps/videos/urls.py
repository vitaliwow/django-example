from django.urls import include, path

app_name = "videos"

urlpatterns = [
    path("v1/", include("apps.videos.api.v1.urls")),
]
