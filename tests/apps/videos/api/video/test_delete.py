import pytest

from apps.videos.models import Video
from core.testing import ApiClient

pytestmark = pytest.mark.django_db


def test_user_delete_video_from_themself_but_not_from_platform_ok(as_user: ApiClient, video: Video) -> None:
    as_user.delete(f"/api/v1/videos/{video.public_id}/")

    assert Video.objects.filter(public_id=video.public_id).first() == video
    assert video.users.filter(pk=as_user.user.pk).exists() is False
