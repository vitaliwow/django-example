import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

from apps.videos.models import VideoFile
from core.models.choices import MaterialsCookStatuses
from core.testing.api import ApiClient
from tests.fixtures.core.api import as_commercial_user

from rest_framework import status

pytestmark = pytest.mark.django_db


def test_list_for_commercial_user_video_file_ok(
    as_commercial_user: ApiClient,
    video_file_root_uri: str,
    video_file_obj: VideoFile,
) -> None:
    video_file_obj.setattr_and_save("user", as_commercial_user.user)

    got = as_commercial_user.get(video_file_root_uri)["results"][0]

    assert got["publicId"]
    assert "mp4" in got["file"]
    assert got["created"]
    assert got["summaryStatus"] == MaterialsCookStatuses.NOT_STARTED
    assert got["shortSummaryStatus"] == MaterialsCookStatuses.NOT_STARTED
    assert got["quizzStatus"] == MaterialsCookStatuses.NOT_STARTED


def test_list_for_staff_returns_all_video_files(
    as_staff: ApiClient,
    video_file_root_uri: str,
    video_file_obj: VideoFile,
) -> None:
    got = as_staff.get(video_file_root_uri)["results"][0]

    assert got["publicId"]
    assert "mp4" in got["file"]
    assert got["created"]
    assert got["summaryStatus"] == MaterialsCookStatuses.NOT_STARTED
    assert got["shortSummaryStatus"] == MaterialsCookStatuses.NOT_STARTED
    assert got["quizzStatus"] == MaterialsCookStatuses.NOT_STARTED


def test_list_fails_for_others(as_user: ApiClient, video_file_root_uri: str, video_file: SimpleUploadedFile) -> None:
    as_user.get(
        video_file_root_uri,
        expected_status=status.HTTP_403_FORBIDDEN,
    )
