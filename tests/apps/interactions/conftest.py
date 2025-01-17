import pytest
from apps.interactions.models import Quiz
from apps.playlists.models import Playlist


@pytest.fixture()
def quiz(playlist: Playlist) -> Quiz:
    return Quiz.objects.create(data={"data": "data"}, playlist=playlist)
