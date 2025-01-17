import pytest
from pytest_mock import MockerFixture
from unittest.mock import Mock

from apps.interactions.models import Quiz
from apps.playlists.api.v1.serializers import PlaylistVideoSerializer
from apps.playlists.models import Playlist
from apps.playlists.services.playlist_video_adder import PlaylistVideoAdder
from apps.summarization.models import Summary, Timecodes
from apps.users.models import User
from apps.videos.models import Video, VideoFile
from rest_framework.exceptions import ValidationError

from tests.factories.apps.playlists import PlaylistFactory
from tests.apps.summarization.example import RESULT, SUMMARIZED

pytestmark = [pytest.mark.django_db]


def test_playlist_add_video(staff: User, playlist: Playlist, ya_video: Video, video: Video) -> None:
    start_playlist = playlist.videos.count()
    data = {
        "videos": [
            {
                "video_public_id": str(ya_video.pk),
                "is_ai_suggested": False,
            },
        ],
    }
    serializer = PlaylistVideoSerializer(data=data)
    upd_playlist = PlaylistVideoAdder(user=staff, playlist=playlist, serializer=serializer)()

    assert upd_playlist.videos.count() == start_playlist + 1
    assert list(upd_playlist.videos.all()) == [ya_video, video]


def test_not_owner_cant_add_video_to_playlist(user: User, playlist: Playlist, ya_video: Video) -> None:
    data = [
        {"video_public_id": str(ya_video.pk), "is_ai_suggested": False},
    ]
    serializer = PlaylistVideoSerializer(data=data, many=True)

    with pytest.raises(ValidationError, match="Only owner can add video to playlist"):
        PlaylistVideoAdder(user=user, playlist=playlist, serializer=serializer)()


def test_playlist_add_ai_video(staff: User, playlist: Playlist, ya_video: Video, video: Video) -> None:
    start_playlist = playlist.videos.count()
    data = {
        "videos": [
            {
                "video_public_id": str(ya_video.pk),
                "is_ai_suggested": True,
            },
        ],
    }

    serializer = PlaylistVideoSerializer(data=data)
    upd_playlist: Playlist = PlaylistVideoAdder(user=staff, playlist=playlist, serializer=serializer)()

    assert upd_playlist.videos.count() == start_playlist + 1
    assert upd_playlist.list_ai_suggested_video_pks == [str(ya_video.pk)]


@pytest.fixture()
def mocked_timecodes_creator_pre_process(mocker: MockerFixture) -> Mock:
    method = mocker.patch(
        "apps.summarization.services.timecodes.from_video_instance.TimecodesCreatorFromVideoInstance.pre_process"
    )
    method.return_value = None
    return method


@pytest.fixture()
def mocked_send_audio_to_bucket(mocker: MockerFixture) -> Mock:
    method = mocker.patch(
        "apps.summarization.services.timecodes.from_video_instance.TimecodesCreatorFromVideoInstance.send_audio_to_bucket"
    )
    method.return_value = "str"
    return method


@pytest.fixture()
def mocked_recognizer(mocker: MockerFixture) -> Mock:
    method = mocker.patch(
        "apps.summarization.services.transcript.transcript_creator.TranscriptCreatorFromVideoFile.get_recognition_data"
    )
    method.return_value = RESULT
    return method


@pytest.fixture()
def mocked_summarizator_response(mocker: MockerFixture) -> Mock:
    method = mocker.patch("apps.summarization.services.summary.summarizer.main.Summarizer.make_full_summary")
    method.return_value = SUMMARIZED
    return method


@pytest.fixture()
def mocked_video_downloader(mocker: MockerFixture, video_file_instance: VideoFile) -> Mock:
    method = mocker.patch("apps.videos.services.video.video_downloader.VideoDownloader.act")
    method.return_value = video_file_instance
    return method


@pytest.fixture()
def mocked_to_ogg_converter(mocker: MockerFixture, video_file_instance: VideoFile) -> Mock:
    method = mocker.patch("apps.videos.services.video.file_converter.VideoConverterToAudio.act")
    method.return_value = video_file_instance
    return method


@pytest.fixture()
def mocked_frames_set_creator(mocker: MockerFixture) -> Mock:
    method = mocker.patch("apps.frames.services.frames_creator.FramesSetCreator.act")
    method.return_value = None
    return method


@pytest.fixture()
def mocked_remove_file(mocker: MockerFixture) -> Mock:
    method = mocker.patch("os.remove")
    method.return_value = None
    return method


@pytest.fixture()
def mocked_get_summary_expenses(mocker: MockerFixture) -> Mock:
    method = mocker.patch(
        "apps.summarization.services.summary.creator.summary_creator.SummaryCreator.get_summary_expenses"
    )
    method.return_value = {'yandex': 10000000}
    return method

@pytest.mark.skip()
@pytest.mark.usefixtures(
    "mocked_timecodes_creator_pre_process",
    "mocked_send_audio_to_bucket",
    "mocked_recognizer",
    "mocked_to_ogg_converter",
    "mocked_get_summary_expenses",
    "mocked_summarizator_response",
    "mocked_pdf_creator",
    "mocked_quiz_generator",
    "mocked_filtering_quiz_generator",
    "mocked_quiz_expenses",
    "mocked_video_downloader",
    "mocked_frames_set_creator",
)
def test_private_playlist_add_video(staff: User, ya_video: Video) -> None:
    init_summaries = Summary.objects.count()
    playlist = PlaylistFactory(owner=staff, privacy_type=Playlist.PrivacyTypeChoices.PRIVATE)
    data = {
        "videos": [
            {
                "video_public_id": str(ya_video.pk),
                "is_ai_suggested": False,
            },
        ],
    }
    serializer = PlaylistVideoSerializer(data=data)

    upd_playlist = PlaylistVideoAdder(user=staff, playlist=playlist, serializer=serializer)()

    summary: Summary = Summary.objects.latest('created')
    quiz: Quiz = Quiz.objects.latest('created')
    timecodes = Timecodes.objects.filter(video=ya_video).first()
    assert upd_playlist.videos.count() == 1
    assert list(upd_playlist.videos.all()) == [ya_video]
    assert init_summaries + upd_playlist.videos.count() == Summary.objects.count()
    assert quiz.video_file == ya_video.video_file
    assert summary.video_file == ya_video.video_file
    assert timecodes.purpose == Timecodes.Purpose.FOR_PRIVATE_PLAYLIST
    assert isinstance(timecodes.data["timecodes"], list)
