import pytest
from apps.summarization.models import Timecodes
from apps.videos.models import VideoFile
from core.testing.api import ApiClient
from django.core.files.base import ContentFile

pytestmark = pytest.mark.django_db


@pytest.mark.skip("fix it")
def test_create_timecode_with_empty_body(as_anon: ApiClient) -> None:
    as_anon.post("/api/v1/timecodes/", expected_status=400)


@pytest.mark.skip("fix it")
def test_timecode_crates_ok(as_anon: ApiClient, video_file: ContentFile) -> None:
    resp = as_anon.post("/api/v1/timecodes/", data={"videofile": video_file}, format="multipart")

    video_file = VideoFile.objects.first()
    timecodes = Timecodes.objects.first()
    assert resp["isPrepared"] is False
    assert resp["data"] is None
    assert resp["publicId"] != ""
    assert video_file is None
    assert timecodes is not None
