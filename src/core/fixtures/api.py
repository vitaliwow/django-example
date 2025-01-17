import pytest

from apps.users.models import User
from core.testing import ApiClient


@pytest.fixture
def as_anon() -> ApiClient:
    return ApiClient()


@pytest.fixture
def as_user(user: User) -> ApiClient:
    return ApiClient(user=user)


@pytest.fixture
def as_commercial_user(commercial_user: User) -> ApiClient:
    return ApiClient(user=commercial_user)
