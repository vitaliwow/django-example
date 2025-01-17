from celery import shared_task

from apps.ai_integration.update_index import UpdateAIIndex


@shared_task(name="videos.rebuild_index")
def rebuild_index_for_video(video_id: str) -> None:
    UpdateAIIndex(video_id=video_id)()
