import pytest
from apps.playlists.models import Category, Playlist
from apps.users.models import User
from apps.videos.models import Video

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


def test_ai_server_request(staff: User, min_data: dict) -> None:
    Playlist.objects.only_commercial().first()
