import pytest
from apps.playlists.models import Playlist
from apps.summarization.models import Summary, Timecodes
from apps.videos.models import Video
from core.testing.api import ApiClient
from django.core.files.base import ContentFile
from rest_framework import status

pytestmark = pytest.mark.django_db


@pytest.fixture()
def summary(timecodes: Timecodes, pdf_file: ContentFile) -> Summary:
    return Summary.objects.create(
        timecodes=timecodes,
        raw_data={"some": "data"},
        pdf_file=pdf_file,
    )


