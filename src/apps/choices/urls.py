from django.urls import include, path

app_name = "choices"

urlpatterns = [
    path("v1/choices/", include("apps.choices.api.v1.urls")),
]
