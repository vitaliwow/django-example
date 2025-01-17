import pytest

from apps.summarization.models import Summary, ShortSummary
from apps.summarization.services.summary.creator.short_summary_creator import ShortSummaryCreator
from apps.videos.models import VideoFile
from core.models.choices import MaterialsCookStatuses

pytestmark = [pytest.mark.django_db]


def test_short_summary_created_from_transcript(
    video_file_instance: VideoFile,
    full_summary_from_video_file: Summary,
) -> None:
    short_summary: "ShortSummary" = ShortSummaryCreator(full_summary=full_summary_from_video_file)()

    video_file_instance.refresh_from_db()
    assert short_summary.video_file == video_file_instance
    assert video_file_instance.short_summary_status == MaterialsCookStatuses.DONE
    assert short_summary.data
