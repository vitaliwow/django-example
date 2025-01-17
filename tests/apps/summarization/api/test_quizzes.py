import pytest
from rest_framework import status

from apps.playlists.models import Playlist
from core.testing.api import ApiClient

from tests.factories.apps.playlists import (
    PlaylistFactory,
    QuizFactory,
    UserFactory,
    VideoFactory,
    PrivateLinksForUsersFactory,
    PrivateLinkFactory,
)


@pytest.mark.django_db()
class TestGet:
    def setup_method(self):
        self.endpoint = "/api/v1/playlists/{playlist_pk}/videos/{video_pk}/quizzes/"
        self.private = Playlist.PrivacyTypeChoices.PRIVATE
        self.public = Playlist.PrivacyTypeChoices.PUBLIC
        self.commercial = Playlist.PrivacyTypeChoices.COMMERCIAL
    """
    def test_it_returns_quizzes_for_private_playlist(self, as_user: ApiClient):
        video = VideoFactory()
        video.users.add(as_user.user)
        playlist = PlaylistFactory(owner=as_user.user, privacy_type=self.private)
        playlist.videos.add(video)
        QuizFactory(playlist=playlist, video=video)
        QuizFactory(playlist=playlist, video=video)
        QuizFactory(playlist=playlist, video=video)

        response = as_user.get(self.endpoint.format(playlist_pk=playlist.pk, video_pk=video.pk))

        assert response['count'] == 3


    def test_it_raises_exc_if_playlist_is_public(self, as_user: ApiClient):
        video = VideoFactory()
        video.users.add(as_user.user)
        playlist = PlaylistFactory(owner=as_user.user, privacy_type=self.public)
        playlist.videos.add(video)
        QuizFactory(playlist=playlist, video=video)
        QuizFactory(playlist=playlist, video=video)
        QuizFactory(playlist=playlist, video=video)

        response = as_user.get(
            self.endpoint.format(playlist_pk=playlist.pk, video_pk=video.pk),
            expected_status=status.HTTP_400_BAD_REQUEST,
        )

        assert response['message'] == f"Playlist has invalid privacy: {playlist.privacy_type}"
    """

    """
    def test_it_raises_exc_if_playlist_is_commercial(self, as_user: ApiClient):
        video = VideoFactory()
        video.users.add(as_user.user)
        playlist = PlaylistFactory(owner=as_user.user, privacy_type=self.commercial)
        playlist.videos.add(video)
        QuizFactory(playlist=playlist, video=video)
        QuizFactory(playlist=playlist, video=video)
        QuizFactory(playlist=playlist, video=video)

        response = as_user.get(
            self.endpoint.format(playlist_pk=playlist.pk, video_pk=video.pk),
            expected_status=status.HTTP_400_BAD_REQUEST,
        )

        assert response['message'] == f"Playlist has invalid privacy: {playlist.privacy_type}"
    """

    """
    def test_it_returns_empty_list_for_non_owner_user(self, as_user: ApiClient):
        user = UserFactory()
        video = VideoFactory()
        video.users.add(user)
        playlist = PlaylistFactory(owner=user, privacy_type=self.private)
        playlist2 = PlaylistFactory(owner=user, privacy_type=self.private)
        playlist.videos.add(video)
        private_link2 = PrivateLinkFactory(playlist=playlist2)
        QuizFactory(playlist=playlist, video=video)
        QuizFactory(playlist=playlist, video=video)
        QuizFactory(playlist=playlist, video=video)
        PrivateLinksForUsersFactory(private_link=private_link2, user=as_user.user)

        response = as_user.get(
            self.endpoint.format(playlist_pk=playlist.pk, video_pk=video.pk),
            expected_status=status.HTTP_400_BAD_REQUEST,
        )

        assert response['message'] == 'The user do not have an access'
    """
