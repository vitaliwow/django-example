import pytest
from apps.summarization.services.speechkit.bucket import BucketObjectSender
from apps.summarization.services.speechkit.recognizer import SpeechRecognizer
from apps.videos.models import VideoFile

pytestmark = pytest.mark.django_db


@pytest.mark.skip("Skip in CI")
@pytest.mark.usefixtures("audio_file")
def test_recognizer(video_file: VideoFile, iam_token: str) -> None:
    file_link = BucketObjectSender(video_file=video_file, token=iam_token)()
    result = SpeechRecognizer(file_link=file_link, iam_token=iam_token)()

    assert isinstance(result, dict)
    assert result["done"] is True
