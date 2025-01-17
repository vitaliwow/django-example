import typing

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import update_last_login
from rest_framework import exceptions
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs: typing.Any) -> None:
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            "password": attrs["password"],
        }

        try:  # noqa: SIM105
            authenticate_kwargs["request"] = self.context["request"]
        except KeyError:
            pass

        self.user = authenticate(**authenticate_kwargs)

        if not self.user:
            User = get_user_model()
            try:
                user_obj = User.objects.get(**{self.username_field: attrs[self.username_field]})
                if not user_obj.is_active:
                    raise exceptions.AuthenticationFailed(
                        "User account is inactive",
                        "no_active_account",
                    )
            except User.DoesNotExist as err:
                raise exceptions.AuthenticationFailed(
                    "No account found with the given credentials",
                    "no_active_account",
                ) from err
            raise exceptions.AuthenticationFailed(
                "No account found with the given credentials",
                "no_active_account",
            )

        if not self.user.is_active:
            raise exceptions.AuthenticationFailed("User account is inactive", "no_active_account")

        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data
