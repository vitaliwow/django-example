import logging
import time
from dataclasses import dataclass
from functools import cached_property

import requests
from django.conf import settings
from requests import Response
from rest_framework.status import HTTP_200_OK

from core.services import BaseService


@dataclass
class UpdateAIIndex(BaseService):
    video_id: str | None = None
    host: str = settings.AI_SEARCH_HOST
    port: str = settings.AI_SEARCH_PORT
    token: str = settings.AI_SEARCH_TOKEN

    def act(self) -> None:
        self.send_request()

    def send_request(self) -> None:
        if self.video_id:
            request_data = {
                "scope": {"ids": [self.video_id]},
                "remove": "all",
                "disable_calc_embeddings": True,
            }
            self.remove_all(request_data)
        else:
            request_data = {"remove": "missing"}
            self.remove_missing(request_data)

    def remove_missing(self, request_data: dict) -> Response:
        return self._update_index_request(request_data)

    def remove_all(self, request_data: dict) -> None:
        response = self._update_index_request(request_data)
        if response.status_code != HTTP_200_OK:
            logging.error(
                f"video - {self.video_id} wasn't updated. Status code = {response.status_code}",
            )

            time.sleep(2)
            self._update_index_request(request_data)

    def _update_index_request(self, request_data: dict) -> Response:
        return requests.post(
            self.url,
            headers={"Authorization": f"Bearer {self.token}"},
            json=request_data,
            timeout=200,
        )

    @cached_property
    def url(self) -> str:
        return f"http://{self.host}:{self.port}/update_index"
