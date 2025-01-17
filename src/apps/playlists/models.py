import random
import string
from typing import TYPE_CHECKING, Any

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import Case, Count, When
from django.utils.translation import gettext_lazy as _

from apps.playlists.api.v1.utils import jwt_encode_dict
from core.conf.api import LEN_PRIVATE_LINK
from core.models.abstracts import TimestampedModel
from core.models.choices import PurposeChoices

if TYPE_CHECKING:
    from apps.users.models import User


class PlaylistQuerySet(models.QuerySet["Playlist"]):
    def for_viewset(self) -> "PlaylistQuerySet":
        return (
            self.select_related("owner")
            .prefetch_related(
                "videos",
                "users",
            )
            .exclude(availability_status=Playlist.StatusChoices.BANNED)
        )

    def for_user(self, user: "User") -> "PlaylistQuerySet":
        return self.filter(owner=user)

    def only_commercial(self) -> "PlaylistQuerySet":
        return self.filter(purpose=PurposeChoices.COMMERCIAL)

    def private(self) -> "PlaylistQuerySet":
        return self.filter(privacy_type=Playlist.PrivacyTypeChoices.PRIVATE)

    def commercial(self) -> "PlaylistQuerySet":
        return self.filter(privacy_type=Playlist.PrivacyTypeChoices.COMMERCIAL)


class Playlist(TimestampedModel):
    class PrivacyTypeChoices(models.TextChoices):
        PRIVATE = "private", _("Private")
        PUBLIC = "public", _("Public")
        COMMERCIAL = "commercial", _("Commercial")

    class StatusChoices(models.TextChoices):
        ACTIVE = "active", _("Active")
        BANNED = "banned", _("Banned")

    objects = models.Manager.from_queryset(PlaylistQuerySet)()

    videos = models.ManyToManyField(to="videos.Video")
    users = models.ManyToManyField(to="users.User", through="interactions.PlaylistInteraction")
    owner = models.ForeignKey(to="users.User", on_delete=models.PROTECT, related_name="owned_playlists")
    category = models.ForeignKey(to="playlists.Category", on_delete=models.PROTECT, null=False)

    title = models.CharField(max_length=150, blank=False)
    description = models.TextField(blank=True)
    background_image = models.ImageField(upload_to="playlists/")
    privacy_type = models.CharField(choices=PrivacyTypeChoices.choices, default=PrivacyTypeChoices.PUBLIC)
    availability_status = models.CharField(choices=StatusChoices.choices, default=StatusChoices.ACTIVE)
    purpose = models.CharField(choices=PurposeChoices.choices, default=PurposeChoices.PERSONAL)
    list_ai_suggested_video_pks = ArrayField(models.CharField(max_length=100), default=list)

    def remove_video_from_list_ai_suggested(self, video_pk: str) -> None:
        if video_pk in self.list_ai_suggested_video_pks:
            self.list_ai_suggested_video_pks.remove(video_pk)
            self.save()

    @property
    def likes_count(self) -> int:
        likes = self.interactions.values("is_liked").aggregate(
            likes=Count(Case(When(is_liked=True, then=1))),
        )

        return likes.get("likes")

    @property
    def viewed_count(self) -> int:
        viewed = self.interactions.values("is_viewed").aggregate(
            viewed=Count(Case(When(is_viewed=True, then=1))),
        )

        return viewed.get("viewed")

    def __str__(self) -> str:
        return f"{self.pk}-{self.title}"

    class Meta:
        ordering = ["created"]
        default_related_name = "playlists"


class Category(TimestampedModel):
    class CategoryChoices(models.TextChoices):
        MOVIES = "movies", "Кино"
        MUSICS = "music", "Музыка"
        SPORTS = "sports", "Спорт"
        HOBBIES = "hobbies", "Хобби"
        FLOWERS = "flowers", "Цветы"
        CHILDREN = "children", "Дети"
        HOME = "home", "Дом"
        HUMOR = "humor", "Юмор"
        USEFUL = "useful", "Полезное"
        PSYCHOLOGY = "psychology", "Психология"
        EDUCATION = "education", "Образование"
        LANGUAGES = "languages", "Языки"
        WORK = "work", "Работа"
        TRAVEL = "travel", "Путешествия"

    name = models.CharField(choices=CategoryChoices.choices, default=CategoryChoices.EDUCATION)
    image = models.ImageField(upload_to="photos/", null=True, blank=True)

    def __str__(self) -> str:
        return self.name


class PrivateLink(TimestampedModel):
    playlist = models.ForeignKey(to="playlists.Playlist", on_delete=models.CASCADE, related_name="private_links")
    lifetime = models.CharField(max_length=256)
    token = models.CharField(max_length=655)
    hash = models.CharField(max_length=10, unique=True, db_index=True)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "playlist_private_links"

    def __str__(self) -> str:
        return self.hash

    @classmethod
    def _create_token(cls, data: dict[str, Any]) -> str:
        encoding_data = {
            "user_id": str(data["user_id"]),
            "playlist_pk": data["playlist_pk"],
            "expires": data["lifetime"],
        }
        return jwt_encode_dict(encoding_data)

    @classmethod
    def _create_hash(cls) -> str:
        return "".join(
            random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits)  # noqa: S311
            for _ in range(LEN_PRIVATE_LINK)
        )


class PrivateLinksForUsers(TimestampedModel):
    private_link = models.ForeignKey("playlists.PrivateLink", on_delete=models.CASCADE)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)

    class Meta:
        db_table = "private_links_for_users"
        unique_together = ["user", "private_link"]


class GPTExpensesReport(TimestampedModel):
    """
    A model for storing spent tokens for operations related to requests to the YandexGPT API
    """

    class OperationTypeChoices(models.TextChoices):
        QUIZ = "quiz", _("Quiz")
        TRANSCRIPT = "transcript", _("Transcript")
        FULL_SUMMARY = "full_summary", _("Full summary")
        SHORT_SUMMARY = "short_summary", _("Short summary")

    units_spent = models.IntegerField()
    type_operation = models.CharField(choices=OperationTypeChoices.choices, default=OperationTypeChoices.QUIZ)
    api_request = models.CharField(max_length=255)

    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="expenses_reports")
    video = models.ForeignKey(
        to="videos.Video",
        on_delete=models.CASCADE,
        related_name="expenses_reports_for_video",
        null=True,
    )
    video_file = models.ForeignKey(
        to="videos.VideoFile",
        on_delete=models.CASCADE,
        related_name="expenses_reports_for_video_file",
        null=True,
    )
    playlist = models.ForeignKey(
        to="playlists.Playlist",
        on_delete=models.CASCADE,
        related_name="expenses_reports_for_playlist",
        null=True,
    )

    class Meta:
        ordering = ["created"]
