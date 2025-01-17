import pytest
from core.testing import ApiClient

pytestmark = [
    pytest.mark.django_db,
]


def test_html(as_user: ApiClient) -> None:
    got = as_user.get("/api/v1/docs/redoc/")

    assert '<redoc spec-url="/api/v1/docs/"></redoc>' in got


def test_json(as_user: ApiClient) -> None:
    got = as_user.get("/api/v1/docs/?format=json")

    assert "openapi" in got


def test_yaml(as_user: ApiClient) -> None:
    got = as_user.get("/api/v1/docs/?format=yaml")

    assert "openapi:" in got
