import pytest
from apps.videos.models import Video

pytestmark = [pytest.mark.django_db]


def test_video_str(video: Video) -> None:
    title = f" - {video.title}" if video.title else ""
    assert str(video) == f"({video.video_id}) " + title
