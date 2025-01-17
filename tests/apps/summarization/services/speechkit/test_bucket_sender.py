import pytest
from apps.summarization.services.speechkit.bucket import BucketObjectSender
from apps.videos.models import Video, VideoFile

pytestmark = pytest.mark.django_db


@pytest.mark.skip("Skip in CI")
@pytest.mark.usefixtures("audio_file")
def test_bucket_sender(video: Video, iam_token: str, video_file: VideoFile) -> None:
    result_url = BucketObjectSender(video_file=video_file, token=iam_token)()

    assert "yandexcloud.net" in result_url
