from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from apps.users.models import User


class UserMeSerializer(ModelSerializer):
    is_commercial = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = [
            "public_id",
            "username",
            "first_name",
            "last_name",
            "avatar",
            "is_commercial",
            "has_access_to_cp",
        ]

        read_only_fields = ("has_access_to_cp",)

    def get_is_commercial(self, obj: User) -> bool:
        return obj.status == User.StatusChoices.COMMERCIAL
