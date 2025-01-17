import typing as t

import pytest
from apps.videos.models import Video
from core.testing import ApiClient

pytestmark = pytest.mark.django_db


@pytest.fixture()
def endpoint() -> str:
    return "/api/v1/videos/"


@pytest.mark.skip()
def test_num_queries_list(as_user: ApiClient, django_assert_num_queries: t.Any, endpoint: str) -> None:
    with django_assert_num_queries(4):
        as_user.get(endpoint)
