import typing as t
from dataclasses import dataclass

from django.contrib.auth.models import AnonymousUser
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from apps.users.models import User
from apps.videos.models import Video
from core.services import BaseService


class VideoUpdateServiceSerializer(ModelSerializer):
    class Meta:
        model = Video
        fields = ["title", "description", "starts_from", "purpose", "status"]


@dataclass
class VideoUpdater(BaseService):
    data: dict[str, t.Any]
    instance: Video
    user: User | AnonymousUser

    def act(self) -> Video:
        return self.update()

    def update(self) -> Video:
        for k, v in self.data.items():
            setattr(self.instance, k, v)
        self.instance.save()
        return self.instance

    def get_validators(self) -> list[t.Callable]:
        return [self.validate_user]

    def validate_user(self) -> None:
        if not self.user.is_staff:
            raise ValidationError(_("Only staff can update video"))
