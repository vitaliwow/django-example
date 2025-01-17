import typing as t

from django.db.models import QuerySet

from apps.users.models import User
from apps.videos.models.abstract import MaterialStatus
from core.models import TimestampedModel, models
from core.models.choices import MaterialsCookStatuses


class VideoFileQuerySet(models.QuerySet["VideoFile"]):
    def for_user(self, user: User) -> QuerySet["VideoFile"]:
        return self.select_related("user").filter(user=user)


class VideoFile(MaterialStatus, TimestampedModel):
    objects = models.Manager.from_queryset(VideoFileQuerySet)()

    file = models.FileField(upload_to="videofile/", max_length=500)
    ogg = models.FileField(null=True)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="video_files", null=True)
    video = models.OneToOneField("videos.Video", on_delete=models.CASCADE, related_name="video_file", null=True)

    class Meta:
        ordering = ["-created"]

    def save(self, *args: t.Any, **kwargs: dict[str, t.Any]) -> None:
        super().save(args, kwargs)

        (
            self.video.update_material_statuses(
                {
                    "quizz_status": MaterialsCookStatuses(self.quizz_status),
                    "short_summary_status": MaterialsCookStatuses(self.short_summary_status),
                    "summary_status": MaterialsCookStatuses(self.summary_status),
                    "transcript_status": MaterialsCookStatuses(self.transcript_status),
                },
            )
            if self.video
            else None
        )
