from datetime import datetime

import jwt
from django.utils import timezone
from rest_framework import serializers
from rest_framework.serializers import ValidationError

from apps.playlists.api.v1.utils import jwt_decode_dict
from apps.playlists.models import PrivateLink
from apps.users.models import User


class BaseTokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=655, required=True)

    def validate_token(self, token: str) -> dict:
        try:
            PrivateLink.objects.get(token=token)
        except PrivateLink.DoesNotExist as err:
            raise ValidationError("Token does not exist") from err
        try:
            encoded_data = jwt_decode_dict(token)
            encoded_data["expires"] = datetime.fromisoformat(encoded_data["expires"])
        except jwt.DecodeError as err:
            raise ValidationError("Token is invalid") from err

        if encoded_data["expires"] < timezone.now() or encoded_data["user_id"] is None:
            raise ValidationError("Link is expired")

        try:
            user = User.objects.get(public_id=encoded_data.pop("user_id"))
        except User.DoesNotExist as err:
            raise ValidationError("Owner does not exist") from err

        encoded_data["user"] = user

        self._validate_user(encoded_data)

        encoded_data["user"] = user
        return encoded_data

    @staticmethod
    def _validate_user(data: dict) -> dict:
        """redefine if need user validation"""
