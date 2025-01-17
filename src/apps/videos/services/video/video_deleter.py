from dataclasses import dataclass

from django.contrib.auth.models import AnonymousUser

from apps.users.models import User
from apps.videos.models import Video
from core.services import BaseService


@dataclass
class VideoDeleter(BaseService):
    video: Video
    user: User | AnonymousUser

    def act(self) -> None:
        if self.user.is_staff or self.user.is_superuser:
            self.video.users.clear()
            self.video.delete()
        else:
            self.video.users.remove(self.user)
