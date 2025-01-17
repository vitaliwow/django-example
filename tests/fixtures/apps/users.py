import typing as t

import pytest
from apps.users.models import User
from django.contrib.auth.models import AnonymousUser

if t.TYPE_CHECKING:
    from core.testing.factory import FixtureFactory


@pytest.fixture()
def user(factory: "FixtureFactory") -> User:
    return factory.user()


@pytest.fixture()
def ya_user(factory: "FixtureFactory") -> User:
    return factory.user()


@pytest.fixture()
def staff(factory: "FixtureFactory") -> User:
    return factory.user(is_staff=True)


@pytest.fixture()
def anon_user() -> AnonymousUser:
    return AnonymousUser()


@pytest.fixture()
def commercial_user(factory: "FixtureFactory") -> User:
    return factory.user(status=User.StatusChoices.COMMERCIAL, has_access_to_cp=True)
