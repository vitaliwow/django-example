import typing as t
from dataclasses import dataclass

from django.contrib.auth.models import AnonymousUser
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError

from apps.users.models import User
from apps.videos.models import Video
from apps.videos.services.video.creators.vk import VKVideoCreator
from apps.videos.services.video.creators.youtube import YouTubeVideoCreator
from apps.videos.tasks import download_transcript
from core.services import BaseService

ALLOWED_ORIGINS = ["vk.com", "youtu", "vkvideo"]


@dataclass
class VideoCreateManager(BaseService):
    data: dict
    user: User | AnonymousUser
    MAX_TITLE_LENGTH = 100

    def act(self) -> Video:
        origin = self.get_origin()

        match origin:
            case Video.OriginChoices.VK:
                video = VKVideoCreator(
                    origin_link=self.video_url,
                    title_length=self.MAX_TITLE_LENGTH,
                )()
            case Video.OriginChoices.YOUTUBE:
                video = YouTubeVideoCreator(
                    origin_link=self.video_url,
                    title_length=self.MAX_TITLE_LENGTH,
                )()

        video.users.add(self.user)

        self.after_creation(video)

        return video

    @staticmethod
    def after_creation(video: Video) -> None:
        if video and not video.transcripts.first():
            download_transcript.delay(video.video_id)

    def get_validators(self) -> list[t.Callable]:
        return [self.validate_link, self.validate_user]

    def validate_link(self) -> None:
        if not [o for o in ALLOWED_ORIGINS if o in self.video_url]:
            raise ValidationError(_("Given link is not in a allowed list"))

    def validate_user(self) -> None:
        if isinstance(self.user, AnonymousUser):
            raise ValidationError("Anonymous cannot add videos")

    @property
    def video_url(self) -> str:
        if self.data.get("origin_link"):
            return self.data.get("origin_link")
        raise ValidationError("There is not origin_link in given data")

    def get_origin(self) -> Video.OriginChoices:
        if any(link in self.video_url for link in ("vk.com", "vkvideo")):
            return Video.OriginChoices.VK
        else:
            return Video.OriginChoices.YOUTUBE
