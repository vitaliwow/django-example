import pytest
from apps.playlists.models import Playlist
from core.testing import ApiClient

pytestmark = pytest.mark.django_db


@pytest.mark.skip("Failed codec")
def test_full_search(as_user: ApiClient, playlist: Playlist) -> None:
    uri = f"/api/v1/playlists/{playlist.pk}/full_search/"
    full_url = uri + "?query=some&onlyTranscripts=1"
    got = as_user.get(full_url)

    assert got
