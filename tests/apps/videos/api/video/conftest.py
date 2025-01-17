import pytest


@pytest.fixture()
def url() -> str:
    return "https://www.youtube.com/watch?v=iC5kU4HDT6I"


@pytest.fixture()
def youtube_url() -> str:
    return "https://www.youtube.com/watch?v=UNOkvk_fMmM"


@pytest.fixture
def youtube_mock_response():
    return {
        "id": "UNOkvk_fMmM",
        "snippet": {
            "title": "Kafka и RabbitMQ - БРОКЕРЫ СООБЩЕНИЙ Простым языком на понятном примере.",
            "description": "Что такое брокеры сообщений (Kafka, RabbitMQ) и как их используют.",
            "thumbnails": {
                "default": {
                    "url": "https://i.ytimg.com/vi/UNOkvk_fMmM/default.jpg",
                    "width": 120,
                    "height": 90
                },
                "medium": {
                    "url": "https://i.ytimg.com/vi/UNOkvk_fMmM/mqdefault.jpg",
                    "width": 320,
                    "height": 180
                },
                "high": {
                    "url": "https://i.ytimg.com/vi/UNOkvk_fMmM/hqdefault.jpg",
                    "width": 480,
                    "height": 360
                },
                "standard": {
                    "url": "https://i.ytimg.com/vi/UNOkvk_fMmM/sddefault.jpg",
                    "width": 640,
                    "height": 480
                },
                "maxres": {
                    "url": "https://i.ytimg.com/vi/UNOkvk_fMmM/maxresdefault.jpg",
                    "width": 1280,
                    "height": 720
                }
            },
        },
        "contentDetails": {
            "duration": "PT17M32S",

        }
    }
