from django.contrib.auth.base_user import AbstractBaseUser
from rest_framework.exceptions import ValidationError

from apps.playlists.api.v1.serializers import PrivateLinkSerializer
from apps.playlists.models import Playlist, PrivateLink, PrivateLinksForUsers


def process_link_hash(link_hash: str, user: AbstractBaseUser, is_filter: bool = False) -> Playlist | bool:
    try:
        link_obj = PrivateLink.objects.get(hash=link_hash)
    except PrivateLink.DoesNotExist as err:
        raise ValidationError({"link": "Link hash does not exist"}) from err
    serializer = PrivateLinkSerializer(data={"token": link_obj.token})
    serializer.is_valid(raise_exception=True)
    validated_data = serializer.validated_data
    if not PrivateLinksForUsers.objects.filter(user=user, private_link=link_obj).exists():
        PrivateLinksForUsers.objects.create(private_link=link_obj, user=user)

    if is_filter:
        return Playlist.objects.filter(
            owner_id=validated_data["token"]["user"].public_id,
            public_id=validated_data["token"]["playlist_pk"],
        ).exists()

    return Playlist.objects.get(
        owner_id=validated_data["token"]["user"].public_id,
        public_id=validated_data["token"]["playlist_pk"],
    )
