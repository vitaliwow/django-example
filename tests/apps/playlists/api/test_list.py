import pytest
from apps.playlists.models import Playlist
from core.testing.api import ApiClient

pytestmark = pytest.mark.django_db


@pytest.fixture()
def uri(playlist: Playlist) -> str:
    return "/api/v1/playlists/"


def test_list_playlist(as_user: ApiClient, uri: str, playlist: Playlist) -> None:
    response = as_user.get(uri)["results"][0]

    assert response["publicId"] == str(playlist.public_id)
    assert response["title"] == playlist.title
    assert response["description"] == playlist.description
    assert response["videos"][0]["publicId"] == str(playlist.videos.first().public_id)
    assert response["availabilityStatus"] == playlist.availability_status
