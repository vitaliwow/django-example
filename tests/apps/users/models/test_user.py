import pytest

from apps.playlists.models import Playlist
from apps.users.models import User
from tests.factories.apps.playlists import UserFactory, PlaylistFactory


@pytest.mark.django_db
class TestUserModel:
    def setup_method(self):
        self.private = Playlist.PrivacyTypeChoices.PRIVATE
        self.commercial = Playlist.PrivacyTypeChoices.COMMERCIAL

    def test_status_change_on_commercial(self):
        user = UserFactory(status=User.StatusChoices.ORDINARY)
        playlist1 = PlaylistFactory(owner=user, privacy_type=self.private)
        playlist2 = PlaylistFactory(owner=user, privacy_type=self.private)
        playlist3 = PlaylistFactory(owner=user, privacy_type=self.commercial)

        user.status = User.StatusChoices.COMMERCIAL
        user.save()
        user.refresh_from_db()
        playlist1.refresh_from_db()
        playlist2.refresh_from_db()
        playlist3.refresh_from_db()

        assert user.status == User.StatusChoices.COMMERCIAL
        assert playlist1.privacy_type == self.commercial
        assert playlist2.privacy_type == self.commercial
        assert playlist3.privacy_type == self.commercial

    def test_status_change_on_ordinary(self):
        user = UserFactory(status=User.StatusChoices.COMMERCIAL)
        playlist1 = PlaylistFactory(owner=user, privacy_type=self.private)
        playlist2 = PlaylistFactory(owner=user, privacy_type=self.commercial)
        playlist3 = PlaylistFactory(owner=user, privacy_type=self.commercial)

        user.status = User.StatusChoices.ORDINARY
        user.save()
        user.refresh_from_db()
        playlist1.refresh_from_db()
        playlist2.refresh_from_db()
        playlist3.refresh_from_db()

        assert user.status == User.StatusChoices.ORDINARY
        assert playlist1.privacy_type == self.private
        assert playlist2.privacy_type == self.private
        assert playlist3.privacy_type == self.private
