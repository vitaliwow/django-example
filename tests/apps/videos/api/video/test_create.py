from unittest.mock import patch

import pytest
from apps.videos.models import Video, Transcript
from core.models.choices import PurposeChoices
from core.testing.api import ApiClient

pytestmark = pytest.mark.django_db


@pytest.fixture()
def data(url: str) -> dict:
    return {"originLink": url}


@pytest.mark.skip("Find correct patch")
def test_create_youtube(as_user: ApiClient, youtube_url: str, youtube_mock_response: dict) -> None:
    path_to_func = "apps.videos.services.video.creators.YouTubeVideoCreator._make_request"
    with patch(path_to_func) as mock_fetch_youtube:
        mock_fetch_youtube.return_value = youtube_mock_response
        got = as_user.post("/api/v1/videos/", data={"originLink": youtube_url})
        assert got["title"] == youtube_mock_response["snippet"]["title"]
        assert got["videoId"] == youtube_mock_response["id"]
        assert got["source"] == Video.OriginChoices.YOUTUBE
        assert got["duration"] == 1052000
        assert got["originLink"] == "https://youtube.com/watch?v=UNOkvk_fMmM"
        assert got["startsFrom"] == 0
        assert got["description"] == youtube_mock_response["snippet"]["description"]
        assert got["purpose"] == PurposeChoices.PERSONAL


@pytest.mark.skip("Use mock instead direct connection")
@pytest.mark.parametrize(
    'link',
    [
        "https://www.youtube.com/watch?v=iC5kU4HDT6I",
        "https://youtu.be/ZedLgAF9aEg",
        "https://youtu.be/uvaO85GbdzA?si=QVnOE78tA-q_ziP3",
    ],
)
def test_all_type_youtube_links(as_user: ApiClient, link: list) -> None:
    got = as_user.post("/api/v1/videos/", data={"originLink": link})
    assert got["source"] == Video.OriginChoices.YOUTUBE


def test_create_vk(as_user: ApiClient, vk_url: str, vk_mock_response: dict) -> None:
    path_to_func = "apps.videos.services.video.creators.vk.VKVideoCreator._make_request"
    with patch(path_to_func) as mock_fetch_vk:
        mock_fetch_vk.return_value = vk_mock_response
        got = as_user.post("/api/v1/videos/", data={"originLink": vk_url})
        assert got["title"] == vk_mock_response["title"]
        assert got["videoId"] == f"{vk_mock_response['owner_id']}_{vk_mock_response['id']}"
        assert got["duration"] == vk_mock_response["duration"] * 1000
        assert got["source"] == Video.OriginChoices.VK
        assert got["originLink"] == "https://vk.com/video_ext.php?oid=-50270859&id=456241272"
        assert got["startsFrom"] == 0
        assert got["description"] == vk_mock_response["description"]
        assert got["purpose"] == PurposeChoices.PERSONAL


@pytest.mark.skip("Use mock instead direct connection")
@pytest.mark.parametrize(
    'link',
    [
        "https://vk.com/video/trends?z=video-220754053_456241515%2Fpl_cat_popular_trends",
        "https://vk.com/video?z=video-57489517_456239331%2Fpl_cat_trends",
        "https://vk.com/video/@vk?z=video-22822305_456239538%2Fclub22822305%2Fpl_-22822305_-2",
    ],
)
def test_all_type_vk_links(as_user: ApiClient, link: list) -> None:
    got = as_user.post("/api/v1/videos/", data={"originLink": link})
    assert got["source"] == Video.OriginChoices.VK
