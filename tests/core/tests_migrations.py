import pytest
from django.core.management import call_command

pytestmark = [pytest.mark.django_db]


def test_for_missing_migrations() -> None:
    result = call_command("makemigrations", check=True, dry_run=True)

    assert not result, result
