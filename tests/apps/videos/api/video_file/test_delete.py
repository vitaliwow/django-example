import pytest

from apps.videos.models import VideoFile
from core.testing.api import ApiClient
from tests.fixtures.core.api import as_commercial_user

from rest_framework import status


pytestmark = pytest.mark.django_db


def test_delete_ok_for_commercial(
    as_commercial_user: ApiClient,
    video_file_detailed_uri: str,
    video_file_obj: VideoFile,
) -> None:
    video_file_obj.setattr_and_save("user", as_commercial_user.user)
    as_commercial_user.delete(video_file_detailed_uri)

    assert VideoFile.objects.filter(pk=video_file_obj.pk).exists() is False


def test_staff_can_delete_video_file(
    as_staff: ApiClient,
    video_file_detailed_uri: str,
    video_file_obj: VideoFile,
) -> None:
    as_staff.delete(video_file_detailed_uri)

    assert VideoFile.objects.filter(pk=video_file_obj.pk).exists() is False


def test_delete_fails_for_others(
    as_user: ApiClient,
    video_file_detailed_uri: str,
    video_file_obj: VideoFile,
) -> None:
    as_user.delete(video_file_detailed_uri, expected_status=status.HTTP_403_FORBIDDEN)
