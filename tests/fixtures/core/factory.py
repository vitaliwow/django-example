import pytest
from core.testing.factory import FixtureFactory


@pytest.fixture()
def factory() -> FixtureFactory:
    return FixtureFactory()
