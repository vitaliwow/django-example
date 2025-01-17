import uuid
from datetime import datetime, timedelta

import pytest
from core.testing import ApiClient
from rest_framework import status

from tests.factories.apps.playlists import PlaylistFactory, PrivateLinkFactory, UserFactory, QuizFactory


@pytest.mark.django_db()
class TestPost:
    def setup_method(self):
        self.endpoint = "/api/v1/playlists/{playlist_id}/create/private-link/"
        self.lifetime = datetime.now() + timedelta(days=30)

    def test_it_creates_private_link(self, as_user: ApiClient):
        playlist = PlaylistFactory(owner=as_user.user)
        data = {"lifetime": self.lifetime}

        as_user.post(self.endpoint.format(playlist_id=playlist.pk), data=data, format="json")

    def test_it_raises_exc_if_private_link_already_exists(self, as_user: ApiClient):
        playlist = PlaylistFactory(owner=as_user.user)
        PrivateLinkFactory(playlist=playlist, lifetime=self.lifetime)

        data = {"lifetime": self.lifetime}

        response = as_user.post(
            self.endpoint.format(playlist_id=playlist.pk),
            expected_status=status.HTTP_400_BAD_REQUEST,
            data=data,
            format="json",
        )
        assert response["token"] == "Private link with the entered data already exists"

    def test_it_raises_exc_if_playlist_does_not_exist(self, as_user: ApiClient):
        PlaylistFactory(owner=as_user.user)

        data = {"lifetime": self.lifetime}

        response = as_user.post(
            self.endpoint.format(playlist_id=f"{uuid.uuid4()}"),
            expected_status=status.HTTP_400_BAD_REQUEST,
            data=data,
            format="json",
        )

        assert response["playlist"] == "The user is not an owner of this playlist"

    def test_it_raises_exc_if_not_owner_creates_private_link(self, as_user: ApiClient):
        owner = UserFactory()
        playlist = PlaylistFactory(owner=owner)

        data = {"lifetime": self.lifetime}

        response = as_user.post(
            self.endpoint.format(playlist_id=playlist.pk),
            expected_status=status.HTTP_400_BAD_REQUEST,
            data=data,
            format="json",
        )

        assert response["playlist"] == "The user is not an owner of this playlist"


@pytest.mark.django_db()
class TestGet:
    def setup_method(self):
        self.endpoint = "/api/v1/playlists/read/private-link/?linkHash={link_hash}"

    def test_it_returns_private_link(self, as_user: ApiClient):
        owner = UserFactory()
        playlist = PlaylistFactory(owner=owner)
        PlaylistFactory(owner=owner)
        PlaylistFactory(owner=owner)
        private_link = PrivateLinkFactory(playlist=playlist)
        link_hash = private_link.hash

        response = as_user.get(self.endpoint.format(link_hash=link_hash))

        assert response["linkHash"] == link_hash
        assert response["publicId"] == str(private_link.playlist_id)

    def test_it_raises_exc_if_link_does_not_exist(self, as_user: ApiClient):
        response = as_user.get(self.endpoint.format(link_hash="string"), expected_status=status.HTTP_400_BAD_REQUEST)

        assert response["link"] == "Link hash does not exist"

    def test_it_returns_quizzes(self, as_user: ApiClient):
        owner = UserFactory()
        playlist = PlaylistFactory(owner=owner)
        PlaylistFactory(owner=owner)
        PlaylistFactory(owner=owner)
        private_link = PrivateLinkFactory(playlist=playlist)
        link_hash = private_link.hash
        QuizFactory(playlist=playlist)
        QuizFactory(playlist=playlist)

        response = as_user.get(self.endpoint.format(link_hash=link_hash))

        assert response["linkHash"] == link_hash
        assert response["publicId"] == str(private_link.playlist_id)
        assert len(response['quizes']) == 2
