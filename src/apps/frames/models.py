from core.models import TimestampedModel, models


class Frame(TimestampedModel):
    frame_set = models.ForeignKey("frames.FrameVideoSet", on_delete=models.CASCADE, related_name="frames")
    name = models.CharField(max_length=100)
    timestamp_s = models.FloatField()
    image = models.ImageField(upload_to="frames/")


class FrameVideoSet(TimestampedModel):
    video = models.ForeignKey("videos.Video", on_delete=models.CASCADE, related_name="framesets")
