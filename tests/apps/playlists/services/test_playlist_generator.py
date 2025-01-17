import pytest
from apps.playlists.models import Category, Playlist
from apps.playlists.services.playlist_creator import PlaylistCreator
from apps.users.models import User
from apps.videos.models import Video
from rest_framework.exceptions import ValidationError

pytestmark = [pytest.mark.django_db]


@pytest.fixture()
def category() -> Category:
    return Category.objects.create()


@pytest.fixture()
def min_data(category: Category, staff: User) -> dict:
    return {
        "title": "Title",
        "owner": staff,
        "category": category,
    }


@pytest.fixture()
def full_data(min_data: dict, video: Video) -> dict:
    return min_data | {
        "description": "DESC",
        "videos": [video],
        "privacy_type": Playlist.PrivacyTypeChoices.PRIVATE,
    }


def test_playlist_create_with_min_data(staff: User, min_data: dict) -> None:
    playlist = PlaylistCreator(**min_data)()

    assert playlist.title == min_data["title"]
    assert playlist.owner == min_data["owner"]
    assert playlist.category == min_data["category"]
    assert playlist.description == ""
    assert list(playlist.videos.all()) == []
    assert playlist.privacy_type == Playlist.PrivacyTypeChoices.PUBLIC


def test_playlist_create_with_full_data(full_data: dict) -> None:
    playlist = PlaylistCreator(**full_data)

    assert playlist.title == full_data["title"]
    assert playlist.owner == full_data["owner"]
    assert playlist.category == full_data["category"]
    assert playlist.description == full_data["description"]
    assert playlist.videos == full_data["videos"]
    assert playlist.privacy_type == full_data["privacy_type"]


def test_playlist_cant_create_by_anon(anon_user: User, min_data: dict) -> None:
    min_data["owner"] = anon_user

    with pytest.raises(ValidationError, match="Anonymous cant create playlists"):
        PlaylistCreator(**min_data)()


@pytest.mark.parametrize(
    "field_name",
    ["title", "owner", "category"],
)
def test_cant_create_without_min_data(min_data: dict, field_name: str) -> None:
    del min_data[field_name]

    with pytest.raises(TypeError):
        PlaylistCreator(**min_data)()
