import typing as t
from dataclasses import dataclass

from rest_framework.exceptions import ValidationError

from apps.users.models import User
from apps.videos.models import VideoFile
from apps.videos.services.video.creators.video_from_videofile import VideoFromVideoFileCreator
from core.models.choices import MaterialsCookStatuses
from core.services import BaseService


@dataclass
class VideoFileCreator(BaseService):
    data: dict
    user: User

    def act(self) -> VideoFile:
        video_file = self.create()

        self.after_creation(video_file)
        return video_file

    def create(self) -> VideoFile:
        return VideoFile.objects.create(**self.data, user=self.user)

    def after_creation(self, video_file: VideoFile) -> None:
        VideoFromVideoFileCreator(video_file=video_file, user=self.user)()
        self.run_creating_materials(video_file)

    def run_creating_materials(self, video_file: VideoFile) -> None:
        video_file.transcript_status = MaterialsCookStatuses.QUEUED
        video_file.save()

    def get_validators(self) -> list[t.Callable]:
        return [
            # self.validate_user_is_commercial,
            # self.validate_extension,  # TODO return
        ]

    def validate_user_is_commercial(self) -> None:
        if self.user.is_staff:
            return
        if self.user.status != User.StatusChoices.COMMERCIAL:
            raise ValidationError("Only commercial User can create video files")

    def validate_extension(self) -> None:
        file = self.data.get("file")
        assert file is not None

        if not file.name.endswith(".mp4"):
            raise ValidationError("Invalid extension, valid extensions are: .mp4")
