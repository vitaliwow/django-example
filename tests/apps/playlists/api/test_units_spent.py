import pytest

from core.testing import ApiClient
from tests.factories.apps.playlists import PlaylistFactory, VideoFactory, GPTExpensesReportFactory, UserFactory


@pytest.mark.django_db()
class TestGet:
    def setup_method(self):
        self.endpoint = "/api/v1/playlists/{playlist_pk}/expenses-report/"

    def test_it_returns_units_spent_for_user_playlist(self, as_user: ApiClient):
        video1 = VideoFactory()
        video2 = VideoFactory()
        video3 = VideoFactory()
        video1.users.add(as_user.user)
        video2.users.add(as_user.user)
        video3.users.add(as_user.user)
        playlist1 = PlaylistFactory(owner=as_user.user)
        playlist2 = PlaylistFactory(owner=as_user.user)
        playlist1.videos.add(video1, video2, video3)
        playlist2.videos.add(video1, video3)
        GPTExpensesReportFactory(
            units_spent=999,
            user=as_user.user,
            video=video1,
            playlist=playlist1,
        )
        GPTExpensesReportFactory(
            units_spent=888,
            user=as_user.user,
            video=video2,
            playlist=playlist1,
        )
        expenses_report = GPTExpensesReportFactory(
            units_spent=555,
            user=as_user.user,
            video=video2,
            playlist=playlist1,
        )

        response = as_user.get(self.endpoint.format(playlist_pk=playlist1.pk))

        assert len(response) == 3
        assert response[0]['unitsSpent'] == expenses_report.units_spent
        assert response[0]['apiRequest'] == expenses_report.api_request
        assert response[0]['typeOperation'] == expenses_report.type_operation

    def test_it_returns_empty_list_for_user_playlist_units_spent(self, as_user: ApiClient):
        user = UserFactory()
        video1 = VideoFactory()
        video2 = VideoFactory()
        video3 = VideoFactory()
        video1.users.add(user)
        video2.users.add(user)
        video3.users.add(user)
        playlist1 = PlaylistFactory(owner=user)
        playlist2 = PlaylistFactory(owner=user)
        playlist1.videos.add(video1, video2, video3)
        playlist2.videos.add(video1, video3)
        GPTExpensesReportFactory(
            units_spent=999,
            user=user,
            video=video1,
            playlist=playlist1,
        )

        response = as_user.get(self.endpoint.format(playlist_pk=playlist1.pk))

        assert len(response) == 0


@pytest.mark.django_db()
class TestGet:
    def setup_method(self):
        self.endpoint = "/api/v1/playlists/expenses-report/"

    def test_it_returns_units_spent_for_user_playlist(self, as_user: ApiClient):
        video1 = VideoFactory()
        video2 = VideoFactory()
        video3 = VideoFactory()
        video1.users.add(as_user.user)
        video2.users.add(as_user.user)
        video3.users.add(as_user.user)
        playlist1 = PlaylistFactory(owner=as_user.user)
        playlist2 = PlaylistFactory(owner=as_user.user)
        playlist1.videos.add(video1, video2, video3)
        playlist2.videos.add(video1, video3)

        GPTExpensesReportFactory(
            units_spent=100,
            user=as_user.user,
            video=video1,
            playlist=playlist1,
        )
        GPTExpensesReportFactory(
            units_spent=200,
            user=as_user.user,
            video=video2,
            playlist=playlist1,
        )
        GPTExpensesReportFactory(
            units_spent=300,
            user=as_user.user,
            video=video2,
            playlist=playlist1,
        )
        GPTExpensesReportFactory(
            units_spent=852,
            user=as_user.user,
            video=video2,
            playlist=playlist2,
        )

        response = as_user.get(self.endpoint)

        assert len(response) == 2
