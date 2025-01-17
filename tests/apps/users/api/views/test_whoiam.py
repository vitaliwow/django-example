import pytest
from rest_framework import status

from apps.users.models import User
from core.testing import ApiClient


@pytest.mark.django_db()
class TestGet:
    def setup_method(self):
        self.endpoint = "/api/v1/users/me/"

    def test_it_returns_user(self, as_user: ApiClient):
        response = as_user.get(self.endpoint)

        assert response['publicId'] == str(as_user.user.public_id)
        assert response['username'] == as_user.user.username
        assert response['firstName'] == as_user.user.first_name
        assert response['lastName'] == as_user.user.last_name

    def test_it_returns_commercial_user(self, as_user: ApiClient):
        as_user.user.status = User.StatusChoices.COMMERCIAL
        as_user.user.save()

        response = as_user.get(self.endpoint)

        assert response['publicId'] == str(as_user.user.public_id)
        assert response['username'] == as_user.user.username
        assert response['firstName'] == as_user.user.first_name
        assert response['lastName'] == as_user.user.last_name
        assert response['isCommercial'] == True

    def test_it_returns_non_commercial_user(self, as_user: ApiClient):
        as_user.user.status = User.StatusChoices.ORDINARY
        as_user.user.save()

        response = as_user.get(self.endpoint)

        assert response['publicId'] == str(as_user.user.public_id)
        assert response['username'] == as_user.user.username
        assert response['firstName'] == as_user.user.first_name
        assert response['lastName'] == as_user.user.last_name
        assert response['isCommercial'] == False

    def test_it_raises_exc_if_user_is_anon(self, as_anon: ApiClient):
        response = as_anon.get(self.endpoint, expected_status=status.HTTP_401_UNAUTHORIZED)

        assert response['detail'] == 'Authentication credentials were not provided.'
