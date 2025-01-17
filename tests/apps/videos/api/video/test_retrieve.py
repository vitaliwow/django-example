import typing as t

import pytest

from apps.playlists.models import Playlist
from apps.videos.models import Video
from core.testing import ApiClient
from tests.factories.apps.playlists import (
    PlaylistFactory,
    QuizFactory,
    VideoFactory,
)

pytestmark = pytest.mark.django_db


@pytest.fixture()
def endpoint(video: Video) -> str:
    return f"/api/v1/videos/{video.public_id}/"

  
@pytest.mark.skip()
def test_num_queries_receive(as_user: ApiClient, django_assert_num_queries: t.Any, endpoint: str) -> None:
    with django_assert_num_queries(7):
        as_user.get(endpoint)


@pytest.mark.django_db()
class TestGet:
    def setup_method(self):
        self.endpoint = "/api/v1/videos/{video_pk}/"
        self.private = Playlist.PrivacyTypeChoices.PRIVATE

    def test_it_returns_quizzes_for_video_in_private_playlist(self, as_user: ApiClient):
        video = VideoFactory()
        video.users.add(as_user.user)
        playlist = PlaylistFactory(owner=as_user.user, privacy_type=self.private)
        playlist.videos.add(video)
        QuizFactory(playlist=playlist, video=video)
        QuizFactory(playlist=playlist, video=video)
        QuizFactory(playlist=playlist, video=video)

        response = as_user.get(self.endpoint.format(video_pk=video.pk))

        assert response['publicId'] == str(video.pk)
        assert len(response['quizIds']) == 3
