import pytest
from rest_framework import status

from apps.playlists.models import Playlist
from core.testing.api import ApiClient

from tests.factories.apps.playlists import PlaylistFactory, QuizFactory, UserFactory

#
# @pytest.mark.django_db()
# class TestGet:
#     def setup_method(self):
#         self.endpoint = "/api/v1/playlists/{playlist_pk}/quizes/"
#         self.private = Playlist.PrivacyTypeChoices.PRIVATE
#         self.public = Playlist.PrivacyTypeChoices.PUBLIC
#         self.commercial = Playlist.PrivacyTypeChoices.COMMERCIAL
#
#     def test_it_returns_quizzes_playlist(self, as_user: ApiClient):
#         playlist = PlaylistFactory(owner=as_user.user, privacy_type=self.private)
#         QuizFactory(playlist=playlist)
#         QuizFactory(playlist=playlist)
#         QuizFactory(playlist=playlist)
#
#         response = as_user.get(self.endpoint.format(playlist_pk=playlist.pk))
#
#         assert response['count'] == 3
#
#     def test_it_raises_exc_if_playlist_is_public(self, as_user: ApiClient):
#         playlist = PlaylistFactory(owner=as_user.user, privacy_type=self.public)
#         QuizFactory(playlist=playlist)
#
#         response = as_user.get(
#             self.endpoint.format(playlist_pk=playlist.pk), expected_status=status.HTTP_400_BAD_REQUEST
#         )
#
#         assert response['message'] == "The playlist does not have quizzes"
#
#     def test_it_raises_exc_if_playlist_is_commercial(self, as_user: ApiClient):
#         playlist = PlaylistFactory(owner=as_user.user, privacy_type=self.commercial)
#         QuizFactory(playlist=playlist)
#
#         response = as_user.get(
#             self.endpoint.format(playlist_pk=playlist.pk), expected_status=status.HTTP_400_BAD_REQUEST
#         )
#
#         assert response['message'] == "The playlist does not have quizzes"
#
#     def test_it_raises_exc_if_playlist_does_not_have_quizzes(self, as_user: ApiClient):
#         playlist = PlaylistFactory(owner=as_user.user, privacy_type=self.private)
#
#         response = as_user.get(
#             self.endpoint.format(playlist_pk=playlist.pk), expected_status=status.HTTP_400_BAD_REQUEST
#         )
#
#         assert response['message'] == "The playlist does not have quizzes"
#
#     def test_it_raises_exc_if_user_is_not_playlist_owner(self, as_user: ApiClient):
#         user = UserFactory()
#         playlist = PlaylistFactory(owner=user, privacy_type=self.private)
#         QuizFactory(playlist=playlist)
#
#         response = as_user.get(
#             self.endpoint.format(playlist_pk=playlist.pk), expected_status=status.HTTP_400_BAD_REQUEST
#         )
#
#         assert response['message'] == "The user do not have an access"
