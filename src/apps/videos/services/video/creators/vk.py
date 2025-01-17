import logging
import re
import typing as t
from dataclasses import dataclass
from functools import cached_property

import vk
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError
from vk.exceptions import VkException

from apps.videos.models import Video
from apps.videos.services.video.creators.helpers import check_is_banned
from apps.videos.services.video.creators.youtube import VideoCreateServiceSerializer
from core.conf.environ import env
from core.services import BaseService

ALLOWED_ORIGINS = ["vk", "vkvideo"]


@dataclass
class VKVideoCreator(BaseService):
    origin_link: str
    title_length: int

    def act(self) -> Video:
        return self.get() or self.create()

    def get(self) -> Video:
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
        duration_ms = self.get_duration_ms(video_data)
        title = str(video_data.get("title", "No title"))

        return {
            "title": title if len(title) < self.title_length else title[:96] + "...",
            "source": Video.OriginChoices.VK,
            "starts_from": 0,
            "origin_link": self.origin_link,
            "video_id": self.video_id,
            "thumbnail_url": self._get_thumbnails(video_data),
            "description": video_data.get("description", "No description"),
            "duration": duration_ms
        }

    def _make_request(self, video_id: str) -> dict:
        try:
            session = vk.API(access_token=env("VK_TOKEN"), v=5.131)
            video_data = session.video.get(videos=video_id)
        except VkException as e:  # noqa: TRY302
            raise e  # noqa: TRY201
        if not len(video_data.get("items")):
            raise ValidationError(_(
                f"No items for this link {self.origin_link}. Source blocks video. No insertion possible."
            ))
        return video_data["items"][0]

    def get_duration_ms(self, video_data: dict) -> int:
        if not video_data.get("duration"):
            logging.error(f"In VK video_id={self.video_id} doesn't contain 'duration'.")
            return 0
        duration_seconds = video_data["duration"]
        duration_ms = duration_seconds * 1000
        return duration_ms

    @staticmethod
    def _get_thumbnails(video_data: dict) -> str:
        try:
            image = video_data.get("image")[-1].get("url", "")
        except TypeError as e:  # noqa: TRY302
            raise e  # noqa: TRY201
        return image

    def get_validators(self) -> list[t.Callable]:
        return [self.validate_link]

    def validate_link(self) -> None:
        if not [o for o in ALLOWED_ORIGINS if o in self.origin_link]:
            raise ValidationError(_("Given link is not in a allowed list"))

    @cached_property
    def video_id(self) -> str:
        url_pattern = "https://vk.com/video_ext.php?oid={oid}&id={id}"
        pattern = re.compile(
            r"(clip|video)(?P<direct>-?\d+_\d+)|video_ext\.php\?.*?oid=(?P<oid>-?\d+).*?id=(?P<id>\d+)",
        )

        match = pattern.search(self.origin_link)
        if not match:
            raise ValidationError(_(f"The vk-link {self.origin_link} is not correct."))
        if match.group("direct"):
            link = match.group("direct")
            video_oid, video_id = match.group("direct").split("_")
            self.origin_link = url_pattern.format(oid=video_oid, id=video_id)
            return link
        if match.group("oid") and match.group("id"):
            self.origin_link = url_pattern.format(oid=match.group("oid"), id=match.group("id"))
            return f"{match.group('oid')}_{match.group('id')}"
        raise ValidationError(_(f"The vk-link {self.origin_link} is not correct."))
