import pytest
from apps.playlists.models import Playlist
from core.testing.api import ApiClient

pytestmark = pytest.mark.django_db


@pytest.fixture()
def uri(playlist: Playlist) -> str:
    return "/api/v1/playlists/generate/"


@pytest.mark.skip("Skip for now")
def test_generate_playlist(as_user: ApiClient, uri: str) -> None:
    data = {
        "title": "Hello World",
    }
    response = as_user.post(uri, data=data)

    assert response
