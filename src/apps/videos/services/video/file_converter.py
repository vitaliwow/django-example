import logging
import os
import shlex
import subprocess
from dataclasses import dataclass
from pathlib import Path

from django.conf import settings
from tornado.process import CalledProcessError

from apps.videos.models import VideoFile
from core.services import BaseService


@dataclass
class VideoConverterToAudio(BaseService):
    """Converts mp4 to audio ogg"""

    video_file_instance: VideoFile
    format: str = "ogg"
    dir_path = Path(settings.MEDIA_ROOT + "videos/audiofile/")

    def act(self) -> VideoFile:
        return self.convert()

    def convert(self) -> VideoFile:
        file_path = Path(settings.MEDIA_ROOT + "videos/" + self.video_file_instance.file.name)

        if not self.dir_path.exists():
            os.makedirs(self.dir_path, exist_ok=True)

        ogg_path = f"{str(self.dir_path)}/{file_path.stem}.ogg"
        cmd = shlex.split(f"ffmpeg -y -i {self.video_file_instance.file.url} -acodec libopus -vn -ac 1 {ogg_path}")
        subprocess.run(cmd, check=True)  # noqa: S603

        self.video_file_instance.ogg.name = str(ogg_path)[len(settings.MEDIA_ROOT) :]
        self.video_file_instance.save()

        return self.video_file_instance
