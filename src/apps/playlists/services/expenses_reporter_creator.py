from dataclasses import dataclass

from apps.playlists.models import GPTExpensesReport, Playlist
from apps.users.models import User
from apps.videos.models import Video, VideoFile
from core.services import BaseService


@dataclass
class ExpensesReporterCreator(BaseService):
    user: User
    media_file: Video | VideoFile
    expenses: dict[str, int]
    type_operation: GPTExpensesReport.OperationTypeChoices.choices
    playlist: Playlist | None = None
    _api_request = None
    _units_spent = None

    @property
    def get_api_request(self) -> str:
        return self._api_request

    @property
    def get_units_spent(self) -> int:
        return self._units_spent

    def act(self) -> None:
        self.format_expenses()
        self.create()

    def format_expenses(self) -> None:
        for api_request, units_spent in self.expenses.items():
            self._api_request = api_request
            self._units_spent = units_spent

    def create(self) -> None:
        data = {
            "units_spent": self.get_units_spent,
            "type_operation": self.type_operation,
            "api_request": self.get_api_request,
            "user": self.user,
        }

        if isinstance(self.media_file, Video):
            data["playlist"] = self.playlist
            data["video"] = self.media_file
        elif isinstance(self.media_file, VideoFile):
            data["video_file"] = self.media_file

        GPTExpensesReport.objects.create(**data)
