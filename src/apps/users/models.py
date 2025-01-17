import typing
from uuid import UUID

from django.contrib.auth.models import AbstractUser
from django.core.validators import validate_ipv46_address
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.playlists.models import Playlist
from core.models import TimestampedModel

DEFAULT_IP_ADDRESS = "127.0.0.1"


class User(AbstractUser, TimestampedModel):
    class StatusChoices(models.TextChoices):
        ORDINARY = "ordinary", _("Ordinary")
        COMMERCIAL = "commercial", _("Commercial")

    avatar = models.ImageField(upload_to="users/avatars/", null=True)
    phone_number = models.CharField(
        verbose_name=_("Phone number"),
        max_length=18,
        blank=True,
    )
    ip_address = models.CharField(
        verbose_name=_("IP address"),
        max_length=15,
        validators=[validate_ipv46_address],
        default=DEFAULT_IP_ADDRESS,
    )
    status = models.CharField(choices=StatusChoices.choices, default=StatusChoices.ORDINARY)
    has_access_to_cp = models.BooleanField(
        _("Control panel"),
        default=False,
        help_text=_("Designates whether the user has an access to the control panel."),
    )

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = ["username"]

    class Meta:
        ordering = ["created"]
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        default_related_name = "users"

    def __str__(self) -> str:
        return self.email

    def get_playlist_ids(self) -> list[UUID]:
        return self.owned_playlists.values_list("public_id", flat=True)

    def change_playlist_type(self: "User") -> None:
        playlists = self.owned_playlists
        to_update = []
        if self.status == self.StatusChoices.COMMERCIAL:
            for playlist in playlists.private():
                playlist.privacy_type = Playlist.PrivacyTypeChoices.COMMERCIAL
                to_update.append(playlist)
        if self.status == self.StatusChoices.ORDINARY:
            for playlist in playlists.commercial():
                playlist.privacy_type = Playlist.PrivacyTypeChoices.PRIVATE
                to_update.append(playlist)
        Playlist.objects.bulk_update(to_update, ["privacy_type"])

    @property
    def is_commercial(self) -> bool:
        return self.status == self.StatusChoices.COMMERCIAL

    @property
    def get_videos_ids(self) -> list[UUID]:
        return self.videos.values_list("public_id", flat=True)

    def save(self, *args: typing.Any, **kwargs: dict) -> None:
        if not kwargs.get("force_insert"):
            self.change_playlist_type()
        if not self.first_name:
            self.first_name = self.username
        if not self.last_name:
            self.last_name = self.username
        super().save(*args, **kwargs)


User._meta.get_field("email")._unique = True  # type: ignore # noqa: SLF001
