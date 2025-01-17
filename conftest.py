import pytest
from celery import Celery
from django.conf import settings
from django.test import override_settings

from core.conf.environ import env

pytest_plugins = [
    "tests.factories.core",
    "tests.fixtures.core",
    "tests.factories.apps.playlists",
    "tests.fixtures.apps.playlists",
    "tests.factories.apps.videos",
    "tests.fixtures.apps.videos",
    "tests.factories.apps.users",
    "tests.fixtures.apps.users",
]

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}


@pytest.fixture(scope="session", autouse=True)
def use_file_storage_backend() -> None:  # noqa: PT004
    with override_settings(STORAGES=STORAGES):
        yield


@pytest.fixture(scope="session")
def django_db_setup() -> None:  # noqa: PT004
    """Fixture to configure Django database settings for pytest-postgresql."""

    settings.DATABASES["default"] = {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgresql",
        "USER": env("DB_USER"),
        "PASSWORD": "postgresql",
        "ATOMIC_REQUESTS": True,
    }


@pytest.fixture(scope="session", autouse=True)
def configure_redis() -> Celery:
    broker_url = "redis://localhost:6379/0"
    celery_app = Celery(broker=broker_url)
    celery_app.conf.update(
        task_always_eager=True,
    )
    return celery_app
