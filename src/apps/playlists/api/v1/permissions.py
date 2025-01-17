from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.views import APIView

from apps.playlists.models import Playlist


class IsPlaylistOwner(IsAuthenticated):
    """
    The request is authenticated as a user, or is a read-only request.
    """

    def has_object_permission(self, request: Request, view: APIView, obj: Playlist) -> bool:
        return request.user == obj.owner
