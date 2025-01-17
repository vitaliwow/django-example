from django.urls import include, path

app_name = "a12n"

urlpatterns = [
    path("v1/auth/", include("apps.a12n.api.v1.urls")),
]
