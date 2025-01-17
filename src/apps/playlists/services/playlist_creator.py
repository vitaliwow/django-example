import typing as t
from dataclasses import dataclass

from django.contrib.auth.models import AnonymousUser, User
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from apps.playlists.models import Category, Playlist
from apps.videos.models import Video
from core.models.choices import PurposeChoices
from core.services import BaseService


class PlaylistServiceCreateSerializer(ModelSerializer):
    class Meta:
        model = Playlist
        fields = [
            "title",
            "description",
            "category",
            "privacy_type",
            "owner",
            "list_ai_suggested_video_pks",
        ]


@dataclass
class PlaylistCreator(BaseService):
    title: str
    owner: User
    category: Category
    description: str = ""
    videos: list[Video] | None = None
    privacy_type: Playlist.PrivacyTypeChoices.choices = Playlist.PrivacyTypeChoices.PUBLIC
    purpose: PurposeChoices = PurposeChoices.PERSONAL

    def act(self) -> Playlist:
        playlist = self.create()

        if self.videos:
            for video in self.videos:
                playlist.videos.add(video.pk)
        return playlist

    def create(self) -> Playlist:
        serializer = PlaylistServiceCreateSerializer(
            data={
                "title": self.title,
                "owner": self.owner.pk,
                "category": self.category.pk,
                "description": self.description,
                "privacy_type": self.privacy_type,
                "users": self.owner.pk,
            },
        )
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return serializer.instance

    def get_validators(self) -> list[t.Callable]:
        return [self.validate_owner]

    def validate_owner(self) -> None:
        if isinstance(self.owner, AnonymousUser):
            raise ValidationError(_("Anonymous cant create playlists"))
