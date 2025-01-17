import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()

pytestmark = pytest.mark.django_db


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def my_user(api_client: APIClient) -> User:
    response = api_client.post(
        "/api/v1/users/",
        data={
            "username": "hello",
            "email": "varabyeu.v@gmail.com",
            "password": "t1e2s3t",
        },
    )
    email = response.data['email']
    user = User.objects.get(email=email)
    return user
