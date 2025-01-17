from dataclasses import dataclass
from operator import itemgetter

from django.db.models import QuerySet, ImageField
from rest_framework import exceptions, serializers

from apps.frames.models import Frame
from apps.videos.models import Video
from core.services import BaseService


class VideoSearchServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = [
            "public_id",
            "title",
            "video_id",
            "starts_from",
            "created",
            "origin_link",
            "thumbnail_url",
        ]


@dataclass
class Formatter(BaseService):
    ai_results: dict

    def act(self) -> list:
        serialized_video_qs = VideoSearchServiceSerializer(self.get_queryset(), many=True)
        result = self.get_mixed_ai_results_with_db_records(serialized_video_qs.data)

        return sorted(result, key=itemgetter("score"), reverse=True)

    def get_queryset(self) -> QuerySet:
        return Video.objects.for_viewset().filter(video_id__in=[r.get("id") for r in self.ai_results])

    def get_mixed_ai_results_with_db_records(self, data: dict) -> dict:
        for item in self.ai_results:
            item_id = item.get("id")
            frameset = self.get_frameset(item_id)

            for serializer_item in data:
                if serializer_item["video_id"] == item_id:
                    serializer_item["score"] = item.get("score")
                    serializer_item["description"] = item.get("description")
                    serializer_item["origin_cues"] = item.get("cues")
                    serializer_item["cues"] = [
                        self.get_parsed_cue(
                            cue,
                            item_id,
                            int(item.get("best_offset_ms") / 1000),
                            frameset,
                            serializer_item["origin_link"],
                        )
                        for cue in item.get("cues")
                    ]
                    del serializer_item["origin_link"]
        return data

    @staticmethod
    def get_frameset(video_id: str) -> QuerySet[Frame]:
        return Frame.objects.filter(frame_set__video__video_id=video_id)

    def get_parsed_cue(
        self,
        cue: dict,
        video_id: str,
        lookup_time: int,
        frameset: QuerySet[Frame],
        origin_link: str,
    ) -> dict:
        data = {
            "timestamp_link": self.get_timestamp(
                link=origin_link,
                video_id=video_id,
                offset_ms=cue.get("start_offset_ms"),
            ),
            "duration_s": self.get_duration(duration_ms=cue.get("duration_ms")),
            "content": cue.get("content"),
        }

        if image := self.get_frame_obj(lookup_time, frameset):
            data["image"] = image.url
        else:
            video: Video = self.get_queryset().filter(video_id=video_id).first()
            if video and video.thumbnail_url:
                data["image"] = self.get_queryset().filter(video_id=video_id).values_list("thumbnail_url").first()[0]
        return data

    @staticmethod
    def get_timestamp(link: str, video_id: str, offset_ms: float) -> str:
        try:
            video = Video.objects.get(video_id=video_id)
            if video.summary_status != 'DONE':
                offset_s = round(offset_ms / 1000)
            else:
                offset_s = round(offset_ms)

        except TypeError as err:
            raise exceptions.ValidationError(
                "Invalid offset_ms value - float or integer required",
            ) from err
        else:
            return f"https://www.youtube.com/watch?v{video_id}&t={offset_s}s"

    @staticmethod
    def get_duration(duration_ms: float) -> int:
        try:
            return round(duration_ms / 1000)
        except TypeError as err:
            raise exceptions.ValidationError("Invalid duration_ms value - float or integer required") from err

    @staticmethod
    def get_frame_obj(moment_s: int, qs: QuerySet[Frame]) -> ImageField | None:
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
