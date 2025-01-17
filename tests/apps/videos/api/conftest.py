import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

from apps.users.models import User
from apps.videos.models import VideoFile


@pytest.fixture()
def video_file_obj(video_file: SimpleUploadedFile, commercial_user: User) -> VideoFile:
    return VideoFile.objects.create(file=video_file, user=commercial_user)


@pytest.fixture()
def video_file_root_uri() -> str:
    return "/api/v1/video-files/"
