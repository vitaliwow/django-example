import pytest
from apps.playlists.models import Category


@pytest.fixture()
def category() -> Category:
    return Category.objects.create()
