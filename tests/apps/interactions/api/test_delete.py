import pytest
from apps.interactions.models import Quiz
from core.testing.api import ApiClient
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND

pytestmark = pytest.mark.django_db


def test_anon_cant_delete(as_anon: ApiClient, uri_detailed: str, quiz: Quiz) -> None:
    as_anon.delete(uri_detailed, expected_status=HTTP_404_NOT_FOUND)


@pytest.mark.skip(reason="Fix test")
def test_user_cant_delete(as_user: ApiClient, uri_detailed: str, quiz: Quiz) -> None:
    as_user.delete(uri_detailed, expected_status=HTTP_400_BAD_REQUEST)


@pytest.mark.skip(reason="Fix test")
def test_staff_cant_deletes_ok(as_staff: ApiClient, uri_detailed: str, quiz: Quiz) -> None:
    as_staff.delete(uri_detailed, expected_status=HTTP_404_NOT_FOUND)
