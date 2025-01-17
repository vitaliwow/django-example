import pytest
from apps.playlists.models import Playlist
from core.testing.api import ApiClient

pytestmark = pytest.mark.django_db


@pytest.mark.usefixtures("playlist", "ya_playlist")
def test_my_playlist2(as_user: ApiClient, playlist: Playlist) -> None:
    response = as_user.get("/api/v1/playlists/my/")

    assert response["count"] == 1
