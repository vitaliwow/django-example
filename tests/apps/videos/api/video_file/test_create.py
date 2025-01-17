import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

from core.models.choices import MaterialsCookStatuses
from core.testing.api import ApiClient
from tests.fixtures.core.api import as_commercial_user

from rest_framework import status

pytestmark = pytest.mark.django_db


def test_create_fails_for_non_commercial(
    as_user: ApiClient, video_file_root_uri: str, video_file: SimpleUploadedFile
) -> None:
    as_user.post(
        video_file_root_uri,
        data={"file": video_file},
        format="multipart",
        expected_status=status.HTTP_403_FORBIDDEN,
    )


def test_non_multipart_deprecated(
    as_commercial_user: ApiClient,
    video_file_root_uri: str,
    video_file: SimpleUploadedFile,
) -> None:
    as_commercial_user.post(
        video_file_root_uri,
        data={"file": video_file},
        expected_status=status.HTTP_400_BAD_REQUEST,
    )


@pytest.mark.skip("Wanted to find ffmpeg")
def test_create_for_commercial_user_video_file_ok(
    as_commercial_user: ApiClient,
    video_file_root_uri: str,
    video_file: SimpleUploadedFile,
) -> None:
    got = as_commercial_user.post(video_file_root_uri, data={"file": video_file}, format="multipart")

    assert got["publicId"]
    assert "mp4" in got["file"]
    assert got["created"]
    assert got["summaryStatus"] == MaterialsCookStatuses.NOT_STARTED
    assert got["shortSummaryStatus"] == MaterialsCookStatuses.NOT_STARTED
    assert got["quizzStatus"] == MaterialsCookStatuses.NOT_STARTED


@pytest.mark.skip()
def test_create_for_staff_video_file_ok(
    as_staff: ApiClient,
    video_file_root_uri: str,
    video_file: SimpleUploadedFile,
) -> None:
    got = as_staff.post(video_file_root_uri, data={"file": video_file}, format="multipart")

    assert got["publicId"]
    assert "mp4" in got["file"]
    assert got["created"]
    assert got["summaryStatus"] == MaterialsCookStatuses.NOT_STARTED
    assert got["shortSummaryStatus"] == MaterialsCookStatuses.NOT_STARTED
    assert got["quizzStatus"] == MaterialsCookStatuses.NOT_STARTED
