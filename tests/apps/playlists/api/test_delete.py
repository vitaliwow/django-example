import pytest
from apps.playlists.models import Playlist
from core.testing import ApiClient

pytestmark = pytest.mark.django_db


def test_delete(as_staff: ApiClient, playlist: Playlist) -> None:
    start_count = Playlist.objects.count()
    as_staff.delete(f"/api/v1/playlists/{playlist.public_id}/")

    assert Playlist.objects.count() == start_count - 1
