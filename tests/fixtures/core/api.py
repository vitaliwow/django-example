from collections.abc import Callable

import pytest
from core.testing.api import ApiClient
from django.contrib.auth.models import User


@pytest.fixture()
def api() -> ApiClient:
    return ApiClient()


@pytest.fixture()
def as_anon() -> ApiClient:
    return ApiClient(anon=True)


@pytest.fixture()
def as_() -> Callable[[User | None], ApiClient]:
    def as_who(user: User | None = None) -> ApiClient:
        return ApiClient(user=user, god_mode=False)

    return as_who


@pytest.fixture()
def as_user(as_: Callable, user: User) -> ApiClient:
    return as_(user)


@pytest.fixture()
def as_staff(staff: User) -> ApiClient:
    return ApiClient(user=staff)


@pytest.fixture()
def as_commercial_user(as_: Callable, user: User) -> ApiClient:
    user.status = "commercial"
    user.has_access_to_cp = True
    user.save()
    return as_(user)


@pytest.fixture()
def as_comm_user(as_: Callable, commercial_user: User) -> ApiClient:
    return as_(commercial_user)
