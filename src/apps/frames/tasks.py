from celery import shared_task

from apps.frames.models import FrameVideoSet
from apps.frames.services.frames_creator import FramesSetCreator
from apps.videos.models import Video


@shared_task(name="videos.create_frames")
def create_frames(video_pk: str) -> FrameVideoSet:
    video = Video.objects.filter(pk=video_pk).first()
    if not video:
        raise AttributeError(f"Video {video_pk} not found")
    return FramesSetCreator(video=video)()
