import json
from abc import abstractmethod

import requests
from django.conf import settings

from core.services import BaseService


class AIClient(BaseService):
    host: str = settings.AI_SEARCH_HOST
    port: int = settings.AI_SEARCH_PORT
    token: str = settings.AI_SEARCH_TOKEN

    def act(self) -> dict | None:
        return self.get_response()

    def get_response(self) -> dict | None:
        with requests.Session() as client:
            response = client.post(
                url=self.get_url(),
                headers=self.get_headers(),
                data=json.dumps(self.get_request_data()),
            )
            if response.ok:
                return json.loads(response.text)
            return None

    @abstractmethod
    def get_url(self) -> str:
        ...

    @abstractmethod
    def get_headers(self) -> dict:
        ...

    @abstractmethod
    def get_request_data(self) -> dict:
        ...

    @property
    def suggest_video_uri(self) -> str:
        return f"http://{self.host}:{self.port}/v2/auto_playlist/make"

    @property
    def full_search_uri(self) -> str:
        return f"http://{self.host}:{self.port}/full_search"

    @property
    def generate_playlist_uri(self) -> str:
        return self.suggest_video_uri
