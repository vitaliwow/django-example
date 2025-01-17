from unittest.mock import Mock

import pytest
from pytest_mock import MockerFixture

from apps.summarization.models import Summary
from apps.summarization.services.summary.creator.full_summary_creator import FullSummaryCreator
from apps.summarization.services.transcript.transcript_creator import TranscriptCreatorFromVideoFile
from apps.videos.models import VideoFile, Transcript
from django.core.files.base import ContentFile

from tests.apps.summarization.example import RESULT, SUMMARIZED
from tests.factories.apps.playlists import ShortSummaryFactory, QuizFactory

pytestmark = [pytest.mark.django_db]


@pytest.fixture()
def video_file() -> ContentFile:
    return ContentFile(bytes([1]), name="video.mp4")


@pytest.fixture()
def text_file() -> ContentFile:
    return ContentFile(bytes([1]), name="video.txt")


@pytest.fixture()
def mocked_get_recognition_data(mocker: MockerFixture) -> Mock:
    method = mocker.patch(
        "apps.summarization.services.transcript.transcript_creator.TranscriptCreatorFromVideoFile.get_recognition_data"
    )
    method.return_value = RESULT
    return method


@pytest.fixture()
def transcript_from_video_file(video_file_instance: VideoFile, mocker: MockerFixture) -> Transcript:
    method = mocker.patch(
        "apps.summarization.services.transcript.transcript_creator.TranscriptCreatorFromVideoFile.get_recognition_data"
    )
    method.return_value = RESULT
    return TranscriptCreatorFromVideoFile(video_file=video_file_instance)()


@pytest.fixture()
def uploaded_text_file() -> VideoFile:
    return VideoFile.objects.create(file=ContentFile(bytes([1]), name="video.txt"))


@pytest.fixture()
def mocked_summarizator_response_for_video_file(mocker: MockerFixture) -> Mock:
    method = mocker.patch(
        "apps.summarization.services.summary.summarizer.main.FromTranscriptSummarizer.make_full_summary"
    )
    method.return_value = SUMMARIZED
    return method


@pytest.fixture()
def full_summary_from_video_file(
    transcript_from_video_file: Transcript,
    mocker: MockerFixture,
    mocked_get_recognition_data: Mock,
    mocked_summarizator_response_for_video_file: Mock,
    mocked_pdf_creator: Mock,
) -> Summary:
    mocker.patch("apps.summarization.tasks.summary.create_full_summary_for_video_file.delay")

    return FullSummaryCreator(transcript=transcript_from_video_file)()


@pytest.fixture()
def short_summary_from_video_file(
    video_file_instance_for_commercial: Transcript,
    mocker: MockerFixture,
    mocked_get_recognition_data: Mock,
    mocked_summarizator_response_for_video_file: Mock,
    mocked_pdf_creator: Mock,
) -> Summary:
    mocker.patch("apps.summarization.tasks.summary.create_short_summary_for_video_file.delay")

    return ShortSummaryFactory(video_file=video_file_instance_for_commercial)


@pytest.fixture()
def quiz_from_video_file(
    video_file_instance_for_commercial: Transcript,
    mocker: MockerFixture,
    mocked_get_recognition_data: Mock,
    mocked_summarizator_response_for_video_file: Mock,
    mocked_pdf_creator: Mock,
) -> Summary:
    mocker.patch("apps.summarization.tasks.summary.create_quiz_for_video_file.delay")

    return QuizFactory(video_file=video_file_instance_for_commercial)
