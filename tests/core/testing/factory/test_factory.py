import typing as t
from unittest.mock import Mock

import pytest
from core.testing import FixtureFactory, register


@pytest.fixture()
def fixture_factory() -> FixtureFactory:
    return FixtureFactory()


@pytest.fixture()
def registered_method(mocker: t.Any) -> Mock:
    mock = mocker.Mock(name="registered_method", return_value="i should be returned after getattr")
    mock.__name__ = "registered_method"
    register(mock)
    return mock


def test_call_getattr_returns_what_method_returned(fixture_factory: FixtureFactory, registered_method: Mock) -> None:
    result = fixture_factory.registered_method()

    assert result == "i should be returned after getattr"


def test_registered_method_called_with_factory_instance(
    fixture_factory: FixtureFactory,
    registered_method: Mock,
) -> None:
    fixture_factory.registered_method(foo=1)  # act

    registered_method.assert_called_with(fixture_factory, foo=1)


def test_cycle_returns_given_method_n_times(
    fixture_factory: FixtureFactory,
    registered_method: Mock,
    mocker: t.Any,
) -> None:
    fixture_factory.cycle(4).registered_method(bar=1)  # act

    registered_method.assert_has_calls(
        calls=[
            mocker.call(fixture_factory, bar=1),
            mocker.call(fixture_factory, bar=1),
            mocker.call(fixture_factory, bar=1),
            mocker.call(fixture_factory, bar=1),
        ],
    )
