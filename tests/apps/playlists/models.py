import pytest
from apps.playlists.models import Playlist
from apps.users.models import User

pytestmark = [pytest.mark.django_db]


def test_for_user(user: User, playlist: Playlist, ya_playlist: Playlist) -> None:
    qs = Playlist.objects.for_user(user)

    assert qs.first().owner == user
