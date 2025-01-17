from dataclasses import dataclass

from apps.users.models import User
from apps.videos.models import Video, VideoFile
from apps.videos.tasks.download_file_s3 import get_duration_videofile
from core.services import BaseService


@dataclass
class VideoFromVideoFileCreator(BaseService):
    video_file: VideoFile
    user: User
    title: str | None = None
    link: str | None = None

    def act(self) -> Video:
        video = self.create()

        self.after_creation(video)
        return video

    def create(self) -> Video:
        video = Video(
            origin_link=self.link if self.link else self.video_file.file.url,
            source=Video.OriginChoices.UPLOADED,
            video_id=self.video_file.pk,
            title=self.title if self.title else self.video_file.file.name,
        )
        video.save()
        video.users.add(self.user)

        return video

    def after_creation(self, video: Video) -> None:
        self.video_file.video = video
        self.video_file.save()
        get_duration_videofile.delay(video.video_id)
