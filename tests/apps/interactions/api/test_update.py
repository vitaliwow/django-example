import pytest
from apps.playlists.models import Playlist
from core.testing.api import ApiClient
from pytest_lazyfixture import lazy_fixture
from rest_framework.status import HTTP_401_UNAUTHORIZED, HTTP_405_METHOD_NOT_ALLOWED

pytestmark = pytest.mark.django_db


@pytest.mark.skip(reason="Fix test")
def test_anon_cant_update(
    as_anon: ApiClient,
    uri_detailed: str,
    quiz: Playlist,
) -> None:
    as_anon.put(uri_detailed, data={"data": "new_data"}, expected_status=HTTP_401_UNAUTHORIZED)


@pytest.mark.skip(reason="Fix test")
@pytest.mark.parametrize("client", [lazy_fixture("as_staff"), lazy_fixture("as_user")])
def test_quiz_cant_be_updated(
    client: ApiClient,
    uri_detailed: str,
    quiz: Playlist,
) -> None:
    client.put(uri_detailed, data={"data": "new_data"}, expected_status=HTTP_405_METHOD_NOT_ALLOWED)
