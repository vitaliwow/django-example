import pytest
from apps.interactions.models import Quiz
from core.testing.api import ApiClient
from pytest_lazyfixture import lazy_fixture

pytestmark = pytest.mark.django_db


@pytest.mark.skip(reason="Fix test")
@pytest.mark.parametrize("client", [lazy_fixture("as_staff"), lazy_fixture("as_user"), lazy_fixture("as_anon")])
def test_retrieve_quiz_ok_for_all_user_types(client: ApiClient, uri_detailed: str, quiz: Quiz) -> None:
    response = client.get(uri_detailed)

    assert response["publicId"] == str(quiz.public_id)
    assert response["data"] == quiz.data
