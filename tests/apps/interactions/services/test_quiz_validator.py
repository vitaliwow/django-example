import pytest
from apps.interactions.services.quiz.validator import QuizValidator
from apps.playlists.models import Playlist
from apps.users.models import User
from rest_framework.exceptions import ValidationError

from tests.fixtures.apps.playlists import playlist

pytestmark = [pytest.mark.django_db]


def test_ok(staff: User, playlist: Playlist) -> None:
    result = QuizValidator(user=staff)()

    assert result is None


def test_anon(anon_user: User, playlist: Playlist) -> None:
    with pytest.raises(ValidationError, match="Anon can't handle quiz"):
        QuizValidator(user=anon_user)()
