from django.urls import include, path

app_name = "a12n"

urlpatterns = [
    path("v1/", include("apps.users.api.v1.urls")),
]
