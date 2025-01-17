import pytest
from apps.playlists.models import Playlist
from apps.videos.models import Video
from core.testing.api import ApiClient

pytestmark = pytest.mark.django_db


@pytest.fixture()
def uri(playlist: Playlist) -> str:
    return f"/api/v1/playlists/{playlist.pk}/suggest-video/"


@pytest.mark.skip("Skip for now")
def test_suggest_video_ok(as_user: ApiClient, uri: str, playlist: Playlist, ya_video: Video) -> None:
    data = {
        "previously_suggested_videos": [ya_video.pk],
    }
    response = as_user.post(uri, data=data)

    assert response
