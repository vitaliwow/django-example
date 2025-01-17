import typing
import uuid

from rest_framework import permissions
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request

from apps.playlists.models import Playlist
from apps.videos.models import Video


class IsCommercialUser(permissions.BasePermission):
    def has_permission(self, request: Request, view: GenericAPIView) -> bool:
        if request.query_params.get("link_hash", None) is not None:
            return True
        if request.user.is_anonymous:
            return False
        user = request.user
        if all([user.is_authenticated, user.is_commercial]):
            return True
        playlist_pk = view.kwargs.get("playlist_pk", "")
        video_pk = view.kwargs.get("video_pk", "")
        if playlist_pk:
            data = {
                "owner": user,
                "public_id": playlist_pk,
                "privacy_type__in": (Playlist.PrivacyTypeChoices.PRIVATE, Playlist.PrivacyTypeChoices.COMMERCIAL),
            }
            if video_pk:
                data["videos"] = video_pk
            return Playlist.objects.filter(**data).exists()
        if video_pk:
            return Video.objects.filter(public_id=video_pk, users=user).exists()
        return True

    def has_object_permission(self, request: Request, view: GenericAPIView, obj: typing.Any) -> bool:
        user = request.user
        if not all([user.is_commercial, user.has_access_to_cp]):
            return False
        video_id = uuid.UUID(view.kwargs["video_pk"])
        return video_id in request.user.get_videos_ids
