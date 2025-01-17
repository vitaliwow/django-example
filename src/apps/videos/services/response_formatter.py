import typing as t
from dataclasses import dataclass
from operator import itemgetter

from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError

from apps.frames.models import Frame
from core.services import BaseService


@dataclass
class ResponseFormatter(BaseService):
    data: dict
    ai_response: list

    def act(self) -> list:
        """Returns sorted data with mixined score value"""
        data_with_score = self.mixin_attrs_to_serialized_data()

        return sorted(data_with_score, key=itemgetter("score"), reverse=True)

    def mixin_attrs_to_serialized_data(self) -> dict:
        """Mixins score and timestamp_link to initial data

        And remove origin link from serialized data
        """
        data = self.data
        for item_ai in self.ai_response:
            frameset = self.get_frameset(item_ai.id)
            for serializer_item in data:
                if serializer_item["video_id"] == item_ai.id:
                    serializer_item["score"] = item_ai.score
                    serializer_item["description"] = item_ai.description
                    serializer_item["origin_cues"] = item_ai.cues
                    serializer_item["cues"] = [
                        self.get_parsed_cue(
                            cue,
                            item_ai.id,
                            int(item_ai.best_offset_ms / 1000),
                            frameset,
                        )
                        for cue in item_ai.cues
                    ]
                    del serializer_item["origin_link"]
        return data

    def get_parsed_cue(self, cue: t.Any, video_id: str, lookup_time: int, frameset: QuerySet[Frame]) -> dict:
        frame_obj = self.get_frame_obj(lookup_time, frameset)
        return {
            "timestamp_link": self.get_timestamp(
                video_id=video_id,
                offset_ms=cue.start_offset_ms,
            ),
            "duration_s": self.get_duration(duration_ms=cue.duration_ms),
            "content": cue.content,
            "image": "/frames/" + str(frame_obj) if frame_obj else None,
        }

    def get_timestamp(self, video_id: str, offset_ms: float) -> str:
        try:
            offset_s = round(offset_ms / 1000)
        except TypeError as err:
            raise ValidationError(
                "Invalid offset_ms value - float or integer required",
            ) from err
        else:
            return f"https://www.youtube.com/watch?v{video_id}&t={offset_s}s"

    def get_duration(self, duration_ms: float) -> int:
        try:
            return round(duration_ms / 1000)
        except TypeError as err:
            raise ValidationError(_("Invalid duration_ms value - float or integer required")) from err

    def get_frame_obj(self, moment_s: int, qs: QuerySet[Frame]) -> Frame | None:
        moment_float = float(moment_s)
        filtered_qs = qs.filter(timestamp_s__range=(moment_float - 5, moment_float + 5))
        try:
            if filtered_qs.exists():
                return filtered_qs.first().image
            if qs.filter(timestamp_s__gte=moment_float).exists():
                return qs.filter(timestamp_s__gte=moment_float).first().image
            return qs.filter(timestamp_s__lte=moment_float).last().image
        except AttributeError:
            return None

    def get_frameset(self, video_id: str) -> QuerySet[Frame]:
        return Frame.objects.filter(frame_set__video__video_id=video_id)
