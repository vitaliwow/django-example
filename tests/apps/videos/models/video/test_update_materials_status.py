import pytest

from apps.videos.models import VideoFile, Video
from core.models.choices import MaterialsStatuses, MaterialsCookStatuses

pytestmark = [pytest.mark.django_db]


def test_update_materials_status(video_file_instance: VideoFile, ya_video: Video) -> None:
    data: MaterialsStatuses = {
        "quizz_status": MaterialsCookStatuses.FAILED,
        "transcript_status": MaterialsCookStatuses.IN_PROGRESS,
        "summary_status": MaterialsCookStatuses.QUEUED,
        "short_summary_status": MaterialsCookStatuses.DONE,
    }

    ya_video.update_material_statuses(data)
    ya_video.save()

    assert ya_video.quizz_status == data["quizz_status"]
    assert ya_video.transcript_status == data["transcript_status"]
    assert ya_video.summary_status == data["summary_status"]
    assert ya_video.short_summary_status == data["short_summary_status"]