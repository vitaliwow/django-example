from unittest.mock import Mock

import pytest
from apps.playlists.models import Playlist
from apps.users.models import User
from apps.videos.models import Video
from core.testing.api import ApiClient
from pytest_mock import MockerFixture

pytestmark = pytest.mark.django_db


@pytest.fixture()
def mocked_download_frames_for_playlist(mocker: MockerFixture) -> Mock:
    return mocker.patch("apps.playlists.tasks.download_frames_for_playlist.delay")


@pytest.fixture()
def mocked_create_timecodes_and_summaries(mocker: MockerFixture) -> Mock:
    return mocker.patch("apps.summarization.tasks.mixed.create_timecodes_and_summaries_for_playlist.delay")


@pytest.fixture()
def mocked_create_frames_timecodes_and_summaries(mocker: MockerFixture) -> Mock:
    return mocker.patch("apps.summarization.tasks.mixed.create_frames_timecodes_and_summaries_for_playlist.delay")


@pytest.fixture()
def uri(playlist: Playlist) -> str:
    return f"/api/v1/playlists/{playlist.pk}/add-video/"


@pytest.fixture()
def user_playlist(playlist: Playlist, user: User) -> Playlist:
    playlist.setattr_and_save("owner", user)
    return playlist


def test_add_video_regular_to_public_playlist(
    as_user: ApiClient,
    uri: str,
    user_playlist: Playlist,
    video: Video,
) -> None:
    response = as_user.post(
        uri,
        data={
            "videos": [
                {
                    "videoPublicId": video.pk,
                    "isAiSuggested": False,
                },
            ],
        },
    )
    assert str(video.pk) in [x["publicId"] for x in response["videos"]]
    assert response["listAiSuggestedVideoPks"] == []


def test_add_video_with_ai_to_public_playlist(
    as_user: ApiClient,
    uri: str,
    user_playlist: Playlist,
    video: Video,
) -> None:
    response = as_user.post(
        uri,
        data={
            "videos": [
                {
                    "videoPublicId": video.pk,
                    "isAiSuggested": True,
                },
            ],
        },
    )
    assert str(video.pk) in [x["publicId"] for x in response["videos"]]
    assert response["listAiSuggestedVideoPks"] == [str(video.pk)]


def test_add_video_to_public_playlist_without_ai_has_empty_suggested_field(
    as_user: ApiClient,
    uri: str,
    user_playlist: Playlist,
    video: Video,
) -> None:
    response = as_user.post(uri, data={"videos": [{"videoPublicId": video.pk}]})

    assert str(video.pk) in [x["publicId"] for x in response["videos"]]
    assert response["listAiSuggestedVideoPks"] == []


def test_add_multiple_regular_videos_to_public_playlist(
    as_user: ApiClient,
    uri: str,
    user_playlist: Playlist,
    video: Video,
    ya_video: Video,
) -> None:
    response = as_user.post(
        uri,
        data={
            "videos": [
                {
                    "videoPublicId": video.pk,
                    "isAiSuggested": False,
                },
                {
                    "videoPublicId": ya_video.pk,
                    "isAiSuggested": False,
                },
            ],
        },
    )

    public_ids = [x["publicId"] for x in response["videos"]]
    assert str(video.pk) in public_ids
    assert str(ya_video.pk) in public_ids
    assert response["listAiSuggestedVideoPks"] == []


def test_add_multiple_suggested_videos_to_public_playlist(
    as_user: ApiClient,
    uri: str,
    user_playlist: Playlist,
    video: Video,
    ya_video: Video,
) -> None:
    response = as_user.post(
        uri,
        data={
            "videos": [
                {
                    "videoPublicId": video.pk,
                    "isAiSuggested": True,
                },
                {
                    "videoPublicId": ya_video.pk,
                    "isAiSuggested": True,
                },
            ],
        },
    )

    public_ids = [x["publicId"] for x in response["videos"]]
    assert str(video.pk) in public_ids
    assert str(ya_video.pk) in public_ids
    assert response["listAiSuggestedVideoPks"] == [str(video.pk), str(ya_video.pk)]


def test_add_mixed_videos_to_public_playlist(
    as_user: ApiClient,
    uri: str,
    user_playlist: Playlist,
    video: Video,
    ya_video: Video,
) -> None:
    response = as_user.post(
        uri,
        data={
            "videos": [
                {
                    "videoPublicId": video.pk,
                    "isAiSuggested": True,
                },
                {
                    "videoPublicId": ya_video.pk,
                    "isAiSuggested": False,
                },
            ],
        },
    )

    public_ids = [x["publicId"] for x in response["videos"]]
    assert str(video.pk) in public_ids
    assert str(ya_video.pk) in public_ids
    assert response["listAiSuggestedVideoPks"] == [str(video.pk)]


@pytest.mark.skip("fix it")
def test_add_video_to_private_playlist_calls_tasks(
    as_user: ApiClient,
    uri: str,
    user_playlist: Playlist,
    video: Video,
    private_playlist: Playlist,
    mocked_create_frames_timecodes_and_summaries: Mock,
) -> None:
    uri = f"/api/v1/playlists/{private_playlist.pk}/add-video/"
    as_user.post(
        uri,
        data={"videos": [{"videoPublicId": video.pk}]},
    )
    mocked_create_frames_timecodes_and_summaries.assert_called_once()
