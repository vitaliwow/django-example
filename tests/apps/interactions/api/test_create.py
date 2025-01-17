import pytest
from core.testing.api import ApiClient
from rest_framework.status import HTTP_404_NOT_FOUND

pytestmark = pytest.mark.django_db


@pytest.fixture()
def quiz_data() -> dict:
    return {"data": "data"}


def test_creates_by_staff(as_staff: ApiClient, uri: str, quiz_data: dict) -> None:
    as_staff.post(uri, data=quiz_data, expected_status=HTTP_404_NOT_FOUND)


def test_create_by_anon(as_anon: ApiClient, uri: str, quiz_data: dict) -> None:
    as_anon.post(uri, data=quiz_data, expected_status=HTTP_404_NOT_FOUND)


def test_create_by_regular_user(as_user: ApiClient, uri: str, quiz_data: dict) -> None:
    as_user.post(uri, data=quiz_data, expected_status=HTTP_404_NOT_FOUND)
