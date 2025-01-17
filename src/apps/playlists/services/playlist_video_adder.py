import typing as t
from dataclasses import dataclass

from django.contrib.auth.models import AnonymousUser, User
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.playlists.models import Playlist
from apps.videos.models import Video, VideoFile
from core.services import BaseService


@dataclass
class PlaylistVideoAdder(BaseService):
    playlist: Playlist
    user: User
    serializer: serializers.Serializer

    def act(self) -> Playlist:
        videos = []
        for item in self.serializer.validated_data.get("videos", []):
            list_ai_video_pks = self.playlist.list_ai_suggested_video_pks
            video: Video = get_object_or_404(Video, pk=item["video_public_id"])

            if video.status == Video.StatusChoices.BANNED or video.is_unavailable:
                continue

            self.playlist.videos.add(video)
            if item["is_ai_suggested"]:
                list_ai_video_pks.append(str(item["video_public_id"]))
            self.playlist.list_ai_suggested_video_pks = list_ai_video_pks
            self.playlist.save()

            videos.append(video)

        self.after_creation(videos)

        return self.playlist

    def get_validators(self) -> list[t.Callable]:
        return [self.validate_user, self.validate_serializer]

    def validate_user(self) -> None:
        if isinstance(self.user, AnonymousUser) or self.user != self.playlist.owner:
            raise ValidationError(_("Only owner can add video to playlist"))

    def validate_serializer(self) -> None:
        self.serializer.is_valid(raise_exception=True)

    def after_creation(self, videos: list[Video]) -> None:
        if self.playlist.privacy_type != Playlist.PrivacyTypeChoices.PRIVATE:
            return
