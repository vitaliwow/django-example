import pytest
from apps.interactions.models import Quiz
from core.testing.api import ApiClient
from pytest_lazyfixture import lazy_fixture

pytestmark = pytest.mark.django_db


@pytest.mark.skip(reason="Fix test")
@pytest.mark.parametrize("client", [lazy_fixture("as_staff"), lazy_fixture("as_user")])
def test_list_quiz_ok_for_auth_users(client: ApiClient, uri: str, quiz: Quiz) -> None:
    response = client.get(uri)["results"]

    assert response[0]["publicId"] == str(quiz.public_id)
    assert response[0]["data"] == quiz.data
