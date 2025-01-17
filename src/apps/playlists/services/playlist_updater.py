import typing as t
from dataclasses import dataclass

from django.contrib.auth.models import AnonymousUser
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from apps.playlists.models import Playlist
from apps.users.models import User
from core.services import BaseService


class PlaylistUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = [
            "title",
            "description",
            "category",
            "privacy_type",
            "users",
            "availability_status",
        ]


@dataclass
class PlaylistUpdater(BaseService):
    instance: Playlist
    user: User
    serializer: PlaylistUpdateSerializer

    def act(self) -> Playlist:
        self.serializer.is_valid(raise_exception=True)
        self.serializer.save()

        return self.serializer.instance

    def get_validators(self) -> list[t.Callable]:
        return [self.validate_user]

    def validate_user(self) -> None:
        if isinstance(self.user, AnonymousUser):
            raise PermissionDenied(_("Anon can access the playlist"))
        if self.user != self.instance.owner:
            raise PermissionDenied(_("Only owner can update playlist"))
