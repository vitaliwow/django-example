import requests
from celery import shared_task
from django.db import transaction

from apps.videos.models import Transcript, Video
from apps.videos.services.transcript_fetcher import SyncTranscriptionAPI
from apps.videos.services.vk_transcript import VkParseTranscriptions
from apps.videos.tasks.update_index import rebuild_index_for_video
from core.conf.environ import env
from core.models.choices import MaterialsCookStatuses


@shared_task(name="videos.download_transcript")
def download_transcript(video_origin_id: str) -> None:
    save_transcript(video_origin_id)
    rebuild_index_for_video.delay(video_origin_id)


def get_raw_transcript(video_origin_id: str) -> dict:
    with SyncTranscriptionAPI() as api_session:  # noqa: SIM117
        with transaction.atomic():
            return api_session.get_transcript_new(video_id=video_origin_id)


def save_transcript(video_origin_id: str) -> None:
    video = Video.objects.get(video_id=video_origin_id)

    with transaction.atomic():
        video.setattr_and_save("transcript_status", MaterialsCookStatuses.QUEUED)
        try:
            video.setattr_and_save("transcript_status", MaterialsCookStatuses.IN_PROGRESS)
            match video.source:
                case Video.OriginChoices.VK:
                    raw_transcript = VkParseTranscriptions(video=video)()
                case Video.OriginChoices.YOUTUBE:
                    raw_transcript = get_raw_transcript(video_origin_id)
                case _:
                    video.setattr_and_save("transcript_status", MaterialsCookStatuses.NOT_STARTED)
                    return

            transcript = Transcript.objects.create(data=raw_transcript, video=video)
            transcript.save()
        except Exception:
            video.setattr_and_save("transcript_status", MaterialsCookStatuses.FAILED)
        else:
            video.setattr_and_save("transcript_status", MaterialsCookStatuses.DONE)


@shared_task(name="videos.download_all_transcripts")
def download_all_transcripts() -> None:
    video_ids = list(Video.objects.filter(transcripts__isnull=True).exclude_banned().values_list("video_id", flat=True))
    for video_id in video_ids:
        save_transcript(video_id)
