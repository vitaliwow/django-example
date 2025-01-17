import pytest
from pytest_mock import MockerFixture
from unittest.mock import Mock

from apps.users.models import User
from apps.videos.models import Transcript, Video
from apps.videos.services.video.creators import VideoCreateManager
from rest_framework.exceptions import ValidationError

pytestmark = [pytest.mark.django_db]


@pytest.fixture()
def url() -> str:
    return "https://www.youtube.com/watch?v=NGWRea-QceQ"

@pytest.fixture()
def mocked_download_transcript(mocker: MockerFixture) -> Mock:
    method = mocker.patch("apps.videos.tasks.download_transcript.download_transcript.delay")
    method.return_value = None
    return method


def test_error_if_disallowed_origin(staff: User) -> None:
    with pytest.raises(ValidationError, match="Given link is not in a allowed list"):
        VideoCreateManager(data={"origin_link": "daylimotion.com/video"}, user=staff)()


def test_error_if_invalid_body(staff: User) -> None:
    with pytest.raises(ValidationError, match="There is not origin_link in given data"):
        VideoCreateManager(data={"video_link": "vk.com/video"}, user=staff)()


@pytest.mark.parametrize(
    "url",
    ["https://www.youtube.com/watch?v=s", "https://www.youtube.com/watch?v=1U9P78rgn-RIs&t=1949s"],
)
def test_create_video_with_invalid_id_in_link(url: str, staff: User) -> None:
    with pytest.raises(ValidationError):
        VideoCreateManager(data={"origin_link": url}, user=staff)()

@pytest.mark.usefixtures("mocked_download_transcript")
@pytest.mark.parametrize(
    "url",
    ["https://www.youtube.com/watch?v=U9P78rgn-RI&t=s1949", "https://www.youtube.com/watch?v=U9P78rgn-RI&t=s"],
)
def test_creation_with_invalid_time(url: str, staff: User) -> None:
    video = VideoCreateManager(data={"origin_link": url}, user=staff)()
    assert video.starts_from == 0


@pytest.mark.skip(reason="no way of currently testing this")
def test_creation_with_anon(anon_user: User, url: str) -> None:
    with pytest.raises(ValidationError, match="Anonymous cannot add videos"):
        VideoCreateManager(data={"origin_link": url}, user=anon_user)()


@pytest.mark.usefixtures("mocked_download_transcript")
def test_video_creates_with_staff_ok(staff: User, url: str) -> None:
    video: Video = VideoCreateManager(data={"origin_link": url}, user=staff)()

    assert video.video_id == "NGWRea-QceQ"


@pytest.mark.usefixtures("mocked_download_transcript")
def test_same_video_not_dowloaded(staff: User, url: str) -> None:
    before_creating = Video.objects.all().count()
    VideoCreateManager(data={"origin_link": url}, user=staff)()
    VideoCreateManager(data={"origin_link": url}, user=staff)()
    video_qs = Video.objects.all()
    assert video_qs.count() == before_creating + 1


@pytest.mark.usefixtures("mocked_download_transcript")
def test_cant_create_already_banned_video(user: User, staff: User, url: str) -> None:
    video = VideoCreateManager(data={"origin_link": url}, user=staff)()
    video.setattr_and_save("status", Video.StatusChoices.BANNED)

    with pytest.raises(ValidationError, match="Cannot add previously banned video"):
        VideoCreateManager(data={"origin_link": url}, user=staff)()
