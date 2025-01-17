import io
import logging
import os
import typing as t
from dataclasses import dataclass
from functools import cached_property
from glob import glob
from pathlib import Path
from shutil import rmtree
from tempfile import mkdtemp
from types import TracebackType

import ffmpeg
from django.conf import settings
from django.core.files import File
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError

from apps.frames.models import Frame, FrameVideoSet
from apps.videos.models import Transcript, Video, VideoFile
from apps.videos.services.video.video_downloader import VideoDownloader
from core.services import BaseService


class ResultDirectory:
    def __init__(self, result_dir: str | None = None) -> None:
        self.result_dir = result_dir
        self.tmp_dir = None

    def __enter__(self) -> str:
        if self.result_dir is None:
            self.tmp_dir = mkdtemp()
            return self.tmp_dir
        Path(self.result_dir).mkdir(parents=True, exist_ok=True)
        return self.result_dir

    def get(self) -> str:
        if self.result_dir is None:
            return self.tmp_dir
        return self.result_dir

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        if self.tmp_dir is not None:
            rmtree(self.tmp_dir)
            self.tmp_dir = None


@dataclass
class FramesSetCreator(BaseService):
    """Create a set of frames to return it with the search text results"""

    video: Video
    frames_dir_path: str = settings.FRAMES_DIR
    WIDTH: int = 640
    HEIGH: int = -2

    def act(self) -> FrameVideoSet:
        """Return a frameset

        If it isn't exist create a new one, otherwise - return existed one
        """
        frame_set = self.get() or self.create()

        self.after_creation(frame_set)

        return frame_set

    def get(self) -> FrameVideoSet | None:
        return self.video.framesets.first()

    @cached_property
    def transcript(self) -> Transcript | None:
        ai_transcripts = self.video.transcripts.filter(source=Transcript.TranscriptOriginChoices.AI)

        return ai_transcripts.first() if ai_transcripts.exists() else self.video.transcripts.first()

    @property
    def frames_path(self) -> str:
        return f"{self.frames_dir_path}video_{self.video.video_id}"

    def get_timestamps_s(self) -> list:
        return [int(float(x["start"])) for x in self.transcript.data.get("cues", [])]

    def create(self) -> FrameVideoSet:
        timestamps_s = self.get_timestamps_s()
        self.make_frames(timestamps_s)

        frame_set = FrameVideoSet.objects.create(video=self.video)
        filenames = glob(f"{self.frames_path}/*.jpg")
        for i, j in enumerate(timestamps_s):
            name = f"{self.video.video_id}_{j}.jpg"
            try:
                with open(filenames[i], "rb") as f:
                    frame = Frame.objects.create(
                        frame_set=frame_set,
                        name=name,
                        timestamp_s=j,
                    )
                    frame.image.save(name, File(io.BytesIO(f.read())))
                    frame.save()
                os.remove(filenames[i])

            except IndexError:
                pass

            except TypeError:
                logging.error(f"Could not create frame {name}")
                raise

        return frame_set

    def make_frames(self, timestamps_s: list[float]) -> None:
        video_file_qs = VideoFile.objects.filter(video=self.video)
        if not video_file_qs.exists():
            video_file: VideoFile = VideoDownloader(video=self.video)()
        else:
            video_file: VideoFile = video_file_qs.first()

        with ResultDirectory(self.frames_path) as res_dir:
            filter_select = "+".join(f"eq(t,{timestamp})" for timestamp in timestamps_s)
            try:
                (
                    ffmpeg.input(video_file.file.url)
                    .filter("select", filter_select)
                    .filter("scale", self.WIDTH, self.HEIGH)
                    .output(str(Path(res_dir) / "%05d.jpg"), q="25", vsync="0")
                    .run()
                )
            except Exception as e:
                logging.error(e)  # noqa: TRY400

    def get_validators(self) -> list[t.Callable]:
        return [self.validate_transcript, ]

    def validate_transcript(self) -> None:
        if not self.transcript:
            raise ValidationError(_("Transcript is not exist"))


    def after_creation(self, frameset: FrameVideoSet) -> None:
        if self.video.thumbnail_url not in ["", None]:
            return None

        middle_chunk_position = len(self.transcript.data["cues"]) // 2
        cue = self.transcript.data["cues"][middle_chunk_position - 1]

        frames_qs = Frame.objects.filter(frame_set=frameset)
        if not frames_qs.exists():
            return None

        frame: Frame = frames_qs.filter(timestamp_s__gte=cue["start"]).first()

        if frame is None:
            frame: Frame = frames_qs.first()

        self.video.thumbnail_url = frame.image.url
        self.video.save()
