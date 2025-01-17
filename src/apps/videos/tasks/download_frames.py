import os

from celery import shared_task

from apps.frames.services.frames_creator import FramesSetCreator
from apps.videos.models import Video, VideoFile
from apps.videos.services.video.video_downloader import VideoDownloader


@shared_task(name="videos.download_frames")
def download_frames(video_origin_id: str) -> None:
    video: Video = Video.objects.get(video_id=video_origin_id)
    video_file: VideoFile = VideoDownloader(video=video)()
    FramesSetCreator(video_id=video_origin_id, video_path=video_file.file.path)()
    os.unlink(video_file.file.path)
