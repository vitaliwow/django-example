import logging
import re
import typing as t
from dataclasses import dataclass
from functools import cached_property

import isodate
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from googleapiclient.discovery import build
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.videos.models import Video
from apps.videos.services.video.creators.helpers import check_is_banned
from core.services import BaseService

ALLOWED_ORIGINS = ["youtube", "youtu"]


class VideoCreateServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = [
            "source",
            "video_id",
            "title",
            "origin_link",
            "starts_from",
            "thumbnail_url",
            "description",
            "status",
            "duration",
        ]


@dataclass
class YouTubeVideoCreator(BaseService):
    origin_link: str
    title_length: int

    def act(self) -> Video:
        return self.get() or self.create()

    def get(self) -> Video | None:
        video_qs = Video.objects.filter(video_id=self.video_id)

        if video_qs.exists() and check_is_banned(video_qs.first()):
            raise ValidationError(_("Failed to add the video because it's already banned"))

        return video_qs.first() if video_qs else None

    def create(self) -> Video:
        video_data = self.receive_data()
        serializer = VideoCreateServiceSerializer(data=video_data)
        serializer.is_valid(raise_exception=True)
        video: Video = serializer.save()

        return video

    def receive_data(self) -> dict:
        video_data = self._make_request(self.video_id)
        snippet_data = self.get_snippet(video_data)
        duration = self.get_duration_ms(video_data)
        title = str(snippet_data.get("title", "No title"))

        return {
            "title": title if len(title) < self.title_length else title[:96] + "...",
            "source": Video.OriginChoices.YOUTUBE,
            "starts_from": self._get_timestamp() or 0,
            "origin_link": f"https://youtube.com/watch?v={self.video_id}",
            "video_id": self.video_id,
            "thumbnail_url": self._get_thumbnails(snippet_data),
            "description": snippet_data["description"],
            "duration": duration
        }

    def _make_request(self, video_id: str) -> dict:
        session = build("youtube", "v3", developerKey=settings.YOUTUBE_API_KEY)

        response = session.videos().list(part="snippet,contentDetails", id=video_id).execute()
        if not len(response["items"]) or response["items"][0]["snippet"]["channelTitle"] == "Epic Fails":
            raise ValidationError(f"Video_id={video_id} doesn't exist. Please check the link={self.origin_link}")
        session.close()
        return response["items"][0]

    def get_snippet(self, video_data: dict) -> dict:
        if not video_data.get("snippet"):
            raise ValidationError(f"In video_id={self.video_id} doesn't contain 'snippet'.")
        return video_data["snippet"]

    def get_duration_ms(self, video_data: dict) -> int:
        if not video_data.get("contentDetails"):
            logging.error(f"In video_id={self.video_id} doesn't contain 'contentDetails'.")
            return 0
        if not video_data["contentDetails"].get("duration"):
            logging.error(f"In Youtube video_id={self.video_id} doesn't contain 'duration'.")
            return 0
        duration = video_data["contentDetails"]["duration"]
        duration_in_seconds = isodate.parse_duration(duration).total_seconds()
        duration_ms = int(duration_in_seconds * 1000)
        return duration_ms

    @staticmethod
    def _get_thumbnails(video_data: dict) -> str:
        thumbnails_data = video_data["thumbnails"]
        size = [size for size in ("standard", "high", "medium", "default") if size in thumbnails_data][0]  # noqa:RUF015

        return "" if not thumbnails_data.get(size, None) else thumbnails_data[size]["url"]

    def _get_timestamp(self) -> int | str | t.Any:
        pattern = r"(?:[?&]t=)(?:(\d+)h)?(?:(\d+)m)?(\d+)s"
        if self.origin_link is None:
            return 0
        match = re.search(pattern, self.origin_link)

        return match.group(1) if match else 0

    def get_validators(self) -> list[t.Callable]:
        return [self.validate_link]

    def validate_link(self) -> None:
        if "/shorts/" in self.origin_link:
            raise ValidationError(_("The YouTube link is invalid"))

    @cached_property
    def video_id(self) -> str:
        pattern = (
            r"(?:https?:\/\/)?(?:www\.)?"
            r"(?:youtube\.com\/(?:v\/|embed\/|watch\?v=|live\/)|youtu\.be\/)"
            r"([a-zA-Z0-9_-]{11})"
        )
        if self.origin_link is None:
            raise ValidationError(_("There is not video ID in given link"))
        match = re.search(pattern, self.origin_link)
        if not match:
            raise ValidationError(_("There is not video ID in given link"))
        return match.group(1)
