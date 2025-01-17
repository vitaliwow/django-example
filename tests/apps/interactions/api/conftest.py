import pytest
from apps.interactions.models import Quiz
from apps.playlists.models import Playlist


@pytest.fixture()
def uri_detailed(simple_playlist: Playlist, quiz: Quiz) -> str:
    return f"/api/v1/playlists/{simple_playlist.pk}/quizes/{quiz.public_id}/"


@pytest.fixture()
def uri(simple_playlist: Playlist) -> str:
    return f"/api/v1/playlists/{simple_playlist.pk}/quizes/"
