import pytest
from apps.playlists.models import Category, Playlist
from core.testing.api import ApiClient

pytestmark = pytest.mark.django_db


@pytest.fixture()
def uri() -> str:
    return "/api/v1/playlists/"


@pytest.fixture()
def min_data(category: Category) -> dict:
    return {"title": "New", "category": category.pk}


@pytest.fixture()
def full_data(min_data: dict) -> dict:
    return min_data | {
        "description": "Descr",
        "privacy_type": Playlist.PrivacyTypeChoices.PUBLIC,
    }


def test_create_min_data(as_user: ApiClient, uri: str, min_data: dict, category: Category) -> None:
    response = as_user.post(uri, data=min_data)

    assert response["publicId"]
    assert response["title"] == min_data["title"]
    assert response["description"] == ""
    assert response["category"]["name"] == category.name
    assert response["category"]["image"] == category.image
    assert response["videos"] == []
    assert response["availabilityStatus"] == Playlist.StatusChoices.ACTIVE.value


def test_create_full_data(as_user: ApiClient, uri: str, full_data: dict, category: Category) -> None:
    response = as_user.post(uri, data=full_data)

    assert response["publicId"]
    assert response["title"] == full_data["title"]
    assert response["description"] == full_data["description"]
    assert response["category"]["name"] == category.name
    assert response["category"]["image"] == category.image
    assert response["videos"] == []
    assert response["availabilityStatus"] == Playlist.StatusChoices.ACTIVE.value
