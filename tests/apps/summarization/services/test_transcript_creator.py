import pytest

from apps.summarization.services.transcript.transcript_creator import TranscriptCreatorFromVideoFile
from apps.videos.models import VideoFile, Transcript
from core.models.choices import MaterialsCookStatuses
from tests.apps.summarization.api.conftest import transcript

pytestmark = [pytest.mark.django_db]


@pytest.mark.usefixtures("mocked_get_recognition_data")
def test_transcript_created_by_recognition(video_file_instance: VideoFile) -> None:
    transcript = TranscriptCreatorFromVideoFile(video_file=video_file_instance)()

    cues = transcript.data.get("cues")
    assert transcript.full_text.startswith(cues[0]["text"])
    assert transcript.video_file == video_file_instance
    assert transcript.video is None
    assert transcript.source == Transcript.TranscriptOriginChoices.AI


@pytest.mark.usefixtures("mocked_get_recognition_data")
def test_video_file_transcript_status_changed(video_file_instance: VideoFile) -> None:
    initial_transcript_status = video_file_instance.transcript_status

    TranscriptCreatorFromVideoFile(video_file=video_file_instance)()

    video_file_instance.refresh_from_db()
    assert initial_transcript_status == MaterialsCookStatuses.NOT_STARTED
    assert video_file_instance.transcript_status == MaterialsCookStatuses.DONE


@pytest.mark.skip()
@pytest.mark.usefixtures("mocked_get_recognition_data")
def test_many_transcripts_for_video_file(video_file_instance: VideoFile, transcript: Transcript) -> None:
    new_transcript = TranscriptCreatorFromVideoFile(video_file=video_file_instance)()

    assert Transcript.objects.count() == len([transcript, new_transcript])
