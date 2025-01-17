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
