import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

from apps.videos.models import Video, VideoFile
from apps.videos.services.video.file_converter import VideoConverterToAudio
from core.services.iam_token import IAMTokenCreator


from pytest_mock import MockerFixture
from unittest.mock import Mock

from tests.apps.summarization.example import RESULT, SUMMARIZED

pytestmark = pytest.mark.django_db


@pytest.fixture()
def iam_token(video: Video) -> None:
    return IAMTokenCreator()()


@pytest.fixture()
def audio_file(video_file: VideoFile, iam_token: str) -> str:
    path = VideoConverterToAudio(video_file_instance=video_file)()
    video_file.refresh_from_db()

    return path
