from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords

from core.models import TimestampedModel, models


class Transcript(TimestampedModel):
    class TranscriptOriginChoices(models.TextChoices):
        INTERNAL = "INTERNAL", _("Internal")
        ORIGINAL = "ORIGINAL", _("Original")
        AI = "AI", _("AI")

    data = models.JSONField(null=True)
    raw_data = models.JSONField(null=True)
    video = models.ForeignKey("videos.Video", on_delete=models.CASCADE, related_name="transcripts", null=True)
    video_file = models.ForeignKey("videos.VideoFile", on_delete=models.CASCADE, related_name="transcripts", null=True)
    source = models.CharField(
        choices=TranscriptOriginChoices.choices,
        default=TranscriptOriginChoices.INTERNAL,
        db_index=True,
    )
    full_text = models.TextField(null=True)

    history = HistoricalRecords()

    class Meta:
        ordering = ["-created"]
