import typing as t

import pytest
from apps.playlists.models import Playlist
from apps.users.models import User
from apps.videos.models import Video

if t.TYPE_CHECKING:
    from core.testing.factory import FixtureFactory


@pytest.fixture()
def simple_playlist(factory: "FixtureFactory", staff: User) -> Playlist:
    return factory.playlist(user=staff, videos=[])


@pytest.fixture()
def playlist(factory: "FixtureFactory", staff: User, video: Video) -> Playlist:
    return factory.playlist(user=staff, videos=[video])


@pytest.fixture()
def ya_playlist(factory: "FixtureFactory", user: User, video: Video) -> Playlist:
    return factory.playlist(user=user, videos=[video])


@pytest.fixture()
def private_playlist(factory: "FixtureFactory", user: User) -> Playlist:
    return factory.playlist(user=user, videos=[], privacy_type=Playlist.PrivacyTypeChoices.PRIVATE)
