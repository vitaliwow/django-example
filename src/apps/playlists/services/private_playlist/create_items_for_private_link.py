from typing import Any

from rest_framework.exceptions import ValidationError

from apps.playlists.models import Playlist, PrivateLink


def get_private_link_hash(data: dict[str, Any]) -> str:
    try:
        playlist = Playlist.objects.get(public_id=data["playlist_pk"], owner=data["user_id"])
    except Playlist.DoesNotExist as err:
        raise ValidationError(detail={"playlist": "The user is not an owner of this playlist"}) from err

    private_link_hash = PrivateLink._create_hash()  # noqa: SLF001
    token = PrivateLink._create_token(data)  # noqa: SLF001

    if PrivateLink.objects.filter(token=token).exists():
        raise ValidationError(detail={"token": "Private link with the entered data already exists"})
    PrivateLink.objects.create(
        playlist=playlist,
        lifetime=data["lifetime"],
        token=token,
        hash=private_link_hash,
    )
    return private_link_hash
