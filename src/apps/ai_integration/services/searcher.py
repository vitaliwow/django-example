import typing as t
from dataclasses import dataclass

from apps.playlists.models import Playlist
from apps.ai_integration.services.ai_client import AIClient


@dataclass
class Searcher(AIClient):
    query: str
    n_results: int = 20
    n_highlight: int = 5
    only_transcripts: int | str = 0
    playlist: Playlist | None = None
    video_id: str | None = None

    def get_url(self) -> str:
        return self.full_search_uri

    def get_headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.token}",
        }

    def get_request_data(self) -> dict:
        payload = {
            "query": self.query,
            "n_results": self.n_results,
            "n_highlight": self.n_highlight,
            "only_transcripts": bool(self.only_transcripts),
        }
        if self.playlist:
            payload.update({"playlist": {"ids": self.get_list_video_ids()}})
        elif self.video_id:
            payload.update({"playlist": {"ids": [self.video_id]}})

        return payload

    def get_list_video_ids(self) -> list:
        return list(self.playlist.videos.values_list("video_id", flat=True))

    def get_validators(self) -> list[t.Callable]:
        return [self.validate_only_transcripts]

    def validate_only_transcripts(self) -> None:
        try:
            self.only_transcripts = int(self.only_transcripts)
        except ValueError:
            self.only_transcripts = 0
        else:
            if self.only_transcripts != 1:
                self.only_transcripts = 0
