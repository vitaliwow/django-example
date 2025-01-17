import io
import logging
from urllib.parse import urlparse, unquote

import ffmpeg
from billiard.exceptions import WorkerLostError
from celery import shared_task
from core.conf.storage import get_file_s3

from apps.videos.models import VideoFile, Video


@shared_task(
    name="videos.update_video_file_from_storage",
    autoretry_for=(WorkerLostError,),
    retry_kwargs={'max_retries': 3,},
)
def update_video_file_from_storage(link: str, video_file_pk: str) -> None:
    """Update pre created VideoFile instance with the real file and materials"""

    parsed_link = urlparse(link)
    bucket_id, object_id = map(unquote, parsed_link.path.lstrip('/').split('/', 1))
    file_s3 = get_file_s3(object_id, bucket_id)
    file = io.BytesIO(file_s3["Body"].read())

    video_file = VideoFile.objects.get(pk=video_file_pk)
    video_file.file.save(object_id, file, save=False)


@shared_task(name="videos.get_duration_videofile")
def get_duration_videofile(video_id: str) -> None:
    video = Video.objects.get(video_id=video_id)
    try:
        probe = ffmpeg.probe(video.origin_link)
        duration = float(probe['format']['duration'])
        duration_ms = int(duration * 1000)
    except ffmpeg._run.Error:
        logging.error(f"Invalid link - {video.origin_link}")
        duration_ms = 0
    video.setattr_and_save("duration", duration_ms)
