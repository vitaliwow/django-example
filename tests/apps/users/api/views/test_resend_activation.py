import pytest
from rest_framework import status

from tests.factories.apps.playlists import UserFactory


@pytest.mark.django_db()
class TestPost:
    def setup_method(self):
        self.endpoint = "/api/v1/users/resend_activation/"

    def test_it_resends_activation(self, as_anon):
        user = UserFactory(is_active=False)
        data = {"email": user.email}
        as_anon.post(self.endpoint, expected_status=status.HTTP_204_NO_CONTENT, data=data, format="json")

    def test_it_raises_error_if_email_already_activated(self, as_anon):
        user = UserFactory(is_active=True)
        data = {"email": user.email}
        response = as_anon.post(self.endpoint, data=data, format="json", expected_status=status.HTTP_400_BAD_REQUEST)

        assert response["message"] == "Email is already activated"
