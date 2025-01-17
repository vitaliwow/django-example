import pytest
from core.testing.factory import FixtureRegistry, register


@pytest.fixture()
def fixture_registry() -> FixtureRegistry:
    return FixtureRegistry()


def test_registry_raises_exception_if_no_method(fixture_registry: FixtureRegistry) -> None:
    with pytest.raises(AttributeError, match=r"Factory method \“not_real\” not found\."):
        fixture_registry.get("not_real")


def test_registry_returns_correct_method_after_register_decorator(fixture_registry: FixtureRegistry) -> None:
    @register
    def some_method_to_add() -> None:
        pass

    method = fixture_registry.get("some_method_to_add")  # act

    assert some_method_to_add == method