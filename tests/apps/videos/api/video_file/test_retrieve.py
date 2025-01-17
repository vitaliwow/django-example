import pytest

from apps.videos.models import VideoFile
from core.models.choices import MaterialsCookStatuses
from core.testing.api import ApiClient
from tests.fixtures.core.api import as_commercial_user

from rest_framework import status


pytestmark = pytest.mark.django_db


def test_get_detailed_ok_for_commercial(
    as_commercial_user: ApiClient,
    video_file_detailed_uri: str,
    video_file_obj: VideoFile,
) -> None:
    video_file_obj.setattr_and_save("user", as_commercial_user.user)

    got = as_commercial_user.get(video_file_detailed_uri)

    assert got["publicId"] == str(video_file_obj.pk)
    assert got["file"].endswith(".mp4")
    assert got["summaryStatus"] == MaterialsCookStatuses.NOT_STARTED
    assert got["shortSummaryStatus"] == MaterialsCookStatuses.NOT_STARTED
    assert got["quizzStatus"] == MaterialsCookStatuses.NOT_STARTED


def test_get_detailed_ok_for_staff(
    as_staff: ApiClient,
    video_file_detailed_uri: str,
    video_file_obj: VideoFile,
) -> None:
    got = as_staff.get(video_file_detailed_uri)

    assert got["publicId"] == str(video_file_obj.pk)
    assert got["file"].endswith(".mp4")
    assert got["summaryStatus"] == MaterialsCookStatuses.NOT_STARTED
    assert got["shortSummaryStatus"] == MaterialsCookStatuses.NOT_STARTED
    assert got["quizzStatus"] == MaterialsCookStatuses.NOT_STARTED


def test_get_detailed_fails_for_others(
    as_user: ApiClient,
    video_file_detailed_uri: str,
    video_file_obj: VideoFile,
) -> None:
    as_user.get(video_file_detailed_uri, expected_status=status.HTTP_403_FORBIDDEN)
