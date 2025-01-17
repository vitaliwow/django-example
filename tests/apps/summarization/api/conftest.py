import pytest

from apps.summarization.models import Timecodes
from apps.users.models import User
from apps.videos.models import Transcript, Video, VideoFile

pytestmark = pytest.mark.django_db


@pytest.fixture()
def transcript(video: Video) -> Transcript:
    return Transcript.objects.create(
        data={"cues": [{"start": 0, "end": 1, "text": "test"}], "text": "test"},
        video=video,
    )


@pytest.fixture()
def timecodes(video: Video) -> Timecodes:
    return Timecodes.objects.create(video=video, data={"timecodes": [{"text": "some", "time": 3.0, "title": "some"}]})


@pytest.fixture()
def video_file_uri(video_file_instance: VideoFile) -> str:
    return f"/api/v2/video-files/{video_file_instance.pk}/"


@pytest.fixture()
def video_file_instance_for_commercial(video_file_instance: VideoFile, commercial_user: User) -> VideoFile:
    video_file_instance.user = commercial_user
    video_file_instance.save()
    return video_file_instance
