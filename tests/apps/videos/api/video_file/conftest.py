import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

from apps.users.models import User
from apps.videos.models import VideoFile


@pytest.fixture()
def video_file_root_uri() -> str:
    return "/api/v1/video-files/"


@pytest.fixture()
def video_file_detailed_uri(video_file_obj: VideoFile, video_file_root_uri: str) -> str:
    return f"{video_file_root_uri}{video_file_obj.pk}/"
