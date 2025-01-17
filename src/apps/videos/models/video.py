from django.utils.translation import gettext_lazy as _

from apps.playlists.models import Playlist
from apps.users.models import User
from apps.videos.models.abstract import MaterialStatus
from core.models import TimestampedModel, models
from core.models.choices import PurposeChoices


class VideoQuerySet(models.QuerySet["Video"]):
    def for_viewset(self) -> models.QuerySet["Video"]:
        return self.prefetch_related("users").exclude_banned().filter(users__isnull=False)

    def for_user(self, user: User) -> models.QuerySet["Video"]:
        return self.filter(users=user)

    def exclude_banned(self) -> models.QuerySet["Video"]:
        return self.exclude(status=Video.StatusChoices.BANNED)

    def for_playlist(self, playlist_pk: Playlist) -> models.QuerySet["Video"]:
        return self.filter(playlists=playlist_pk)


class Video(MaterialStatus, TimestampedModel):
    class OriginChoices(models.TextChoices):
        YOUTUBE = "YOUTUBE", "YouTube"
        VK = "VK", "VK"
        UPLOADED = "UPLOADED", "Uploaded"

    class StatusChoices(models.TextChoices):
        ON_MODERATION = "ON_MODERATION", (_("On moderation"))
        ACTIVE = "ACTIVE", (_("Active"))
        BANNED = "BANNED", (_("Banned"))

    objects = models.Manager.from_queryset(VideoQuerySet)()

    video_id = models.CharField(max_length=100, unique=True)
    title = models.CharField(max_length=100, blank=True)
    description = models.CharField(max_length=5000, blank=True)
    duration = models.IntegerField(default=0, help_text="Duration in milliseconds")
    source = models.CharField(choices=OriginChoices.choices, default=OriginChoices.YOUTUBE)
    origin_link = models.CharField(max_length=500)
    thumbnail_url = models.CharField(max_length=500)
    starts_from = models.IntegerField(default=0)
    purpose = models.CharField(choices=PurposeChoices.choices, default=PurposeChoices.PERSONAL)
    status = models.CharField(choices=StatusChoices.choices, default=StatusChoices.ACTIVE)
    is_unavailable = models.BooleanField(default=False)
    users = models.ManyToManyField(to="users.User", related_name="videos")

    class Meta:
        ordering = ["-created"]
        default_related_name = "videos"

    def __str__(self) -> str:
        title = f" - {self.title}" if self.title else ""
        return f"({self.video_id}) " + title
