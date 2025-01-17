import typing as t
from datetime import datetime as stock_datetime

import pytest
from django.utils import timezone


@pytest.fixture
def datetime() -> t.Callable[..., stock_datetime]:
    """Create a timezoned datetime"""

    def _f(*args: t.Any, **kwargs: t.Any) -> stock_datetime:
        if isinstance(args[0], int):
            tz = timezone.get_current_timezone()
        else:
            tz = args[0]
            args = args[1:]

        return timezone.make_aware(
            stock_datetime(*args, **kwargs),  # noqa: DTZ001
            timezone=tz,
        )

    return _f
