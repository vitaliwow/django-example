from django.urls import path
from rest_framework_simplejwt import views

app_name = "a12n"


urlpatterns = [
    path("login/", views.TokenObtainPairView.as_view()),
    path("refresh/", views.TokenRefreshView.as_view()),
    path("token-verify/", views.TokenVerifyView.as_view()),
    path("logout/", views.TokenBlacklistView.as_view()),
]
