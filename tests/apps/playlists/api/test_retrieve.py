import pytest
from rest_framework import status

from apps.playlists.models import Playlist
from core.testing.api import ApiClient
from tests.factories.apps.playlists import PlaylistFactory, UserFactory, QuizFactory

pytestmark = pytest.mark.django_db


@pytest.fixture()
def uri_simple(simple_playlist: Playlist) -> str:
    return f"/api/v1/playlists/{simple_playlist.pk}/"


@pytest.fixture()
def uri(playlist: Playlist) -> str:
    return f"/api/v1/playlists/{playlist.pk}/"


def test_retrieve_simple_playlist(as_user: ApiClient, uri_simple: str, simple_playlist: Playlist) -> None:
    response = as_user.get(uri_simple)

    assert response["publicId"] == str(simple_playlist.public_id)
    assert response["title"] == simple_playlist.title
    assert response["description"] == simple_playlist.description
    assert response["videos"] == list(simple_playlist.videos.all())
    assert response["availabilityStatus"] == simple_playlist.availability_status


def test_retrieve_playlist(as_user: ApiClient, uri: str, playlist: Playlist) -> None:
    response = as_user.get(uri)

    assert response["publicId"] == str(playlist.public_id)
    assert response["title"] == playlist.title
    assert response["description"] == playlist.description
    assert response["videos"][0]["publicId"] == str(playlist.videos.first().public_id)
    assert response["availabilityStatus"] == playlist.availability_status


@pytest.mark.django_db()
class TestGet:
    def setup_method(self):
        self.endpoint = "/api/v1/playlists/{playlist_pk}/"
        self.private = Playlist.PrivacyTypeChoices.PRIVATE
        self.public = Playlist.PrivacyTypeChoices.PUBLIC
        self.commercial = Playlist.PrivacyTypeChoices.COMMERCIAL

    def test_it_returns_commercial_playlist(self, as_user: ApiClient):
        playlist = PlaylistFactory(owner=as_user.user, privacy_type=self.commercial)

        response = as_user.get(self.endpoint.format(playlist_pk=playlist.pk))

        assert response['publicId'] == str(playlist.pk)

    def test_it_returns_public_playlist(self, as_user: ApiClient):
        playlist = PlaylistFactory(owner=as_user.user, privacy_type=self.public)

        response = as_user.get(self.endpoint.format(playlist_pk=playlist.pk))

        assert response['publicId'] == str(playlist.pk)

    def test_it_returns_private_playlist_for_owner(self, as_user: ApiClient):
        playlist = PlaylistFactory(owner=as_user.user, privacy_type=self.private)

        response = as_user.get(self.endpoint.format(playlist_pk=playlist.pk))

        assert response['publicId'] == str(playlist.pk)

    def test_it_returns_quiz_ids_for_private_playlist(self, as_user: ApiClient):
        playlist = PlaylistFactory(owner=as_user.user, privacy_type=self.private)
        QuizFactory(playlist=playlist)
        QuizFactory(playlist=playlist)
        QuizFactory(playlist=playlist)

        response = as_user.get(self.endpoint.format(playlist_pk=playlist.pk))

        assert response['publicId'] == str(playlist.pk)
        assert len(response['quizes']) == 3
