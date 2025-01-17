from django.urls import path

from . import views

app_name = "choices"

urlpatterns = [
    path("purpose-choices/", views.PurposeAPIView.as_view()),
]
