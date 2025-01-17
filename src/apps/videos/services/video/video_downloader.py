import io
import logging
import os
import subprocess
from dataclasses import dataclass
from functools import cached_property

from django.conf import settings
from django.core.files import File

from apps.videos.models import Video, VideoFile
from core.exceptions.video_download import VideoDownloadError
from core.services import BaseService


@dataclass
class VideoDownloader(BaseService):
    """Downloads a video and saves as a VideoFile instance

    It DOES NOT REMOVE the downloaded file from given path
    """

    video: Video
    proxy: str = settings.VIDEO_DOWNLOAD_PROXY

    def act(self) -> VideoFile | None:
        path = self.download()

        return self.create_video_file_instance(path) if path else None

    def download(self) -> str | None:
        try:
            if self.video is not None:
                output_path = os.path.join(settings.MEDIA_ROOT, self.video_name)
                result = subprocess.run(  # noqa: S603
                    [  # noqa
                        "yt-dlp",
                        "--proxy",
                        self.proxy,
                        "-f",
                        "w",
                        "-o",
                        output_path,
                        self.video.origin_link,
                    ],
                    capture_output=True,
                    text=True,
                    check=False,
                )
                logging.info(f"yt-dlp command output: {result.stdout}")
                logging.info(f"yt-dlp command code -------: {result.returncode}")
                if result.returncode != 0:
                    # exclude the video from iteration over playlists
                    self.video.is_unavailable = True
                    self.video.save()

                    raise VideoDownloadError(f"Couldn't upload file:- {result.stderr} ")  # noqa
                return output_path

        except subprocess.CalledProcessError as err:
            raise VideoDownloadError(f"Cannot download video from {self.video.origin_link}") from err
        except VideoDownloadError:
            raise
        except Exception as e:
            raise VideoDownloadError(f"An unexpected error occurred: {e!s}") from e

    def create_video_file_instance(self, path: str) -> VideoFile:
        with open(path, "rb") as f:
            file = File(io.BytesIO(f.read()), name=self.video_name)
            return VideoFile.objects.create(video=self.video, file=file)

    @cached_property
    def video_name(self) -> str:
        return f"{self.video.source}_{self.video.video_id}.mp4"
