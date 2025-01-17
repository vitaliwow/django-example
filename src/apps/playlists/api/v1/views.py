import typing
from datetime import timedelta

from django.utils import timezone
from drf_spectacular.utils import OpenApiParameter, extend_schema, inline_serializer
from rest_framework import serializers, status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.playlists.api.v1.serializers import PlaylistRetrieveSerializer
from apps.playlists.models import PrivateLink
from apps.playlists.services.private_playlist.create_items_for_private_link import get_private_link_hash
from apps.playlists.services.private_playlist.get_by_link_hash import process_link_hash


@extend_schema(
    tags=["playlists"],
    request=inline_serializer(
        name="lifetime",
        fields={
            "lifetime": serializers.DateTimeField(default=timezone.now() + timedelta(days=30)),
        },
    ),
)
class PrivateLinkCreateAPIView(CreateAPIView):
    queryset = PrivateLink.objects.all()
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, *args: typing.Any, **kwargs: dict) -> Response:
        link_hash = get_private_link_hash(
            {
                "user_id": self.request.user.pk,
                "lifetime": self.request.data["lifetime"],
                "playlist_pk": self.kwargs["playlist_pk"],
            },
        )
        return Response({"link_hash": link_hash}, status=status.HTTP_201_CREATED)


@extend_schema(
    tags=["playlists"],
    parameters=[
        OpenApiParameter(
            name="link_hash",
            location=OpenApiParameter.QUERY,
            description="Hash of private link",
            required=True,
            type=str,
        ),
    ],
)
class PrivateLinkAPIView(APIView):
    queryset = PrivateLink.objects.all()
    serializer_class = PlaylistRetrieveSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, *args: typing.Any, **kwargs: dict) -> Response:
        link_hash = request.query_params["link_hash"]
        playlist = process_link_hash(link_hash, request.user)
        serializer = self.serializer_class(playlist)
        response_data = serializer.data
        response_data["link_hash"] = link_hash

        return Response(response_data, status=status.HTTP_200_OK)
