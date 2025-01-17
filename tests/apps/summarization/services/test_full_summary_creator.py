import pytest

from apps.summarization.models import Summary
from apps.summarization.services.summary.creator.full_summary_creator import FullSummaryCreator
from apps.videos.models import VideoFile, Transcript
from core.models.choices import MaterialsCookStatuses

pytestmark = [pytest.mark.django_db]


@pytest.mark.usefixtures(
    "mocked_get_recognition_data",
    "mocked_summarizator_response_for_video_file",
    "mocked_pdf_creator",
)
def test_full_summary_created_from_transcript(
    video_file_instance: VideoFile, transcript_from_video_file: Transcript
) -> None:
    full_summary: "Summary" = FullSummaryCreator(transcript=transcript_from_video_file)()

    video_file_instance.refresh_from_db()
    assert full_summary.video_file == video_file_instance
    assert video_file_instance.summary_status == MaterialsCookStatuses.DONE
    assert full_summary.pdf_file is not None
    assert full_summary.markdown is not None
