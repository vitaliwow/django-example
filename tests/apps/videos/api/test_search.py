import pytest
from apps.videos.models import Video
from core.testing import ApiClient
from rest_framework import status

pytestmark = pytest.mark.django_db


@pytest.fixture()
def endpoint(video: Video) -> str:
    return f"/api/v1/videos/{video.public_id}/"


@pytest.mark.skip(reason="no way of currently testing this")
def test_full_search_empty_queryparam(as_user: ApiClient, endpoint: str, video: Video) -> None:
    as_user.get("/api/v1/full-search/", expected_status=status.HTTP_400_BAD_REQUEST)


@pytest.mark.skip(reason="no way of currently testing this")
def test_full_search(as_user: ApiClient, endpoint: str, video: Video) -> None:
    got = as_user.get("/api/v1/full-search/?query=привет")

    assert got
