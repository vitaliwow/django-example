import pytest

from apps.users.models import User
from apps.videos.models import VideoFile
from apps.videos.services.video.creators.video_file import VideoFileCreator

from django.db.models import FileField
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.exceptions import ValidationError

from core.models.choices import MaterialsCookStatuses

pytestmark = [pytest.mark.django_db]


@pytest.mark.skip(reason="TODO")
def test_video_file_cant_be_created_for_regular_user(user: User) -> None:
    file = bytes("video.mp4", "utf-8")
    with pytest.raises(ValidationError):
        VideoFileCreator(
            data={"file": file},
            user=user,
        )()


@pytest.mark.skip(reason="TODO")
def test_video_files_creates_ok(commercial_user: User) -> None:
    filename = "file"
    ext = "mp4"
    file = SimpleUploadedFile(
        f"{filename}.{ext}",
        bytes("file_content", encoding="utf-8"),
        content_type="video/mp4",
    )
    video_file_obj: VideoFile = VideoFileCreator(
        data={"file": file},
        user=commercial_user,
    )()

    assert video_file_obj.user == commercial_user
    assert video_file_obj.file.name.endswith(ext)
    assert filename in video_file_obj.file.name
    assert video_file_obj.ogg == FileField()
    assert video_file_obj.transcript_status == MaterialsCookStatuses.QUEUED
    assert video_file_obj.short_summary_status == MaterialsCookStatuses.NOT_STARTED
    assert video_file_obj.summary_status == MaterialsCookStatuses.NOT_STARTED
    assert video_file_obj.quizz_status == MaterialsCookStatuses.NOT_STARTED


@pytest.mark.skip(reason="TODO")
def test_extension_validation(commercial_user: User, video_file: SimpleUploadedFile) -> None:
    video_file.name = "file.mp3"

    with pytest.raises(ValidationError):
        VideoFileCreator(
            data={"file": video_file},
            user=commercial_user,
        )()
