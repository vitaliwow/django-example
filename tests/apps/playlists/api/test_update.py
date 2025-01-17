import typing as t

import pytest
from apps.playlists.models import Playlist
from apps.users.models import User
from apps.videos.models import Video
from core.testing.api import ApiClient

pytestmark = pytest.mark.django_db


@pytest.fixture()
def uri_simple(simple_playlist: Playlist) -> str:
    return f"/api/v1/playlists/{simple_playlist.pk}/"


@pytest.fixture()
def uri(playlist: Playlist) -> str:
    return f"/api/v1/playlists/{playlist.pk}/"


@pytest.fixture()
def user_playlist(playlist: Playlist, user: User) -> Playlist:
    playlist.setattr_and_save("owner", user)
    return playlist


@pytest.mark.parametrize(
    ("fieldname", "initial", "expected"),
    [
        ("title", "Old title", "New title"),
        ("description", "Old description", "New description"),
    ],
)
def test_playlist_update_regular_fields(  # noqa: PLR0913
    as_user: ApiClient,
    uri: str,
    user_playlist: Playlist,
    fieldname: str,
    initial: t.Any,
    expected: t.Any,
) -> None:
    user_playlist.setattr_and_save(fieldname, initial)

    response = as_user.patch(uri, data={fieldname: expected})

    assert response[fieldname] == expected


def test_playlist_update_privacy_type(
    as_user: ApiClient,
    uri: str,
    user_playlist: Playlist,
) -> None:
    user_playlist.setattr_and_save("privacy_type", Playlist.PrivacyTypeChoices.PRIVATE)

    response = as_user.patch(uri, data={"privacyType": Playlist.PrivacyTypeChoices.PUBLIC})

    assert response["privacyType"] == Playlist.PrivacyTypeChoices.PUBLIC


def test_playlist_update_status(
    as_user: ApiClient,
    uri: str,
    user_playlist: Playlist,
) -> None:
    user_playlist.setattr_and_save("availabilityStatus", Playlist.StatusChoices.ACTIVE)

    response = as_user.patch(uri, data={"availabilityStatus": Playlist.StatusChoices.BANNED})

    assert response["availabilityStatus"] == Playlist.StatusChoices.BANNED.value


def test_cant_add_video(
    as_user: ApiClient,
    uri: str,
    user_playlist: Playlist,
    video: Video,
    ya_video: Video,
) -> None:
    response = as_user.patch(uri, data={"video": ya_video.pk})

    assert str(ya_video.pk) not in response["videos"]


def test_cant_add_users(
    as_user: ApiClient,
    uri: str,
    user_playlist: Playlist,
    ya_user: User,
) -> None:
    response = as_user.patch(uri, data={"users": ya_user.pk})

    assert str(ya_user.pk) not in response["videos"]
