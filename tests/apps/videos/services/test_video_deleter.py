import pytest
from apps.users.models import User
from apps.videos.models import Video
from apps.videos.services.video.video_deleter import VideoDeleter

pytestmark = [pytest.mark.django_db]


def test_soft_delete(video: Video, staff: User) -> None:
    VideoDeleter(video=video, user=staff)()

    assert Video.objects.filter(pk=video.pk).first() is None
