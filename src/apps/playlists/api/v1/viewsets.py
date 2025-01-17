import typing as t
from uuid import UUID

from django.db.models import QuerySet, Sum
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.response import Response

from apps.playlists.api.v1.filtersets import PlaylistsFilterset
from apps.playlists.api.v1.permissions import IsPlaylistOwner
from apps.playlists.api.v1.serializers import (
    CategorySerializer,
    ExpensesReportDetailSerializer,
    InteractionsCreateSerializer,
    InteractionsRetrieveSerializer,
    PlaylistCreateSerializer,
    PlaylistGenerateSerializer,
    PlaylistRetrieveSerializer,
    PlaylistUpdateSerializer,
    PlaylistVideoDeleteSerializer,
    PlaylistVideoSerializer,
    SuggestVideoSerializer,
    TotalExpensesReportSerializer,
    VideoSuggestSerializer,
)
from apps.playlists.models import Category, GPTExpensesReport, Playlist
from apps.ai_integration.services.formatter import Formatter
from apps.ai_integration.services.searcher import Searcher
from apps.playlists.services.playlist_creator import PlaylistCreator
from apps.playlists.services.playlist_updater import PlaylistUpdater
from apps.playlists.services.playlist_video_adder import PlaylistVideoAdder
from apps.videos.models import Video
from core.api.viewsets import DefaultModelViewSet, ReadonlyModelViewSet


@extend_schema_view(
    search=extend_schema(
        parameters=[
            OpenApiParameter(
                name="query",
                location=OpenApiParameter.QUERY,
                description="Query to lookup through the playlist",
                required=False,
                type=str,
            ),
            OpenApiParameter(
                name="only_transcripts",
                location=OpenApiParameter.QUERY,
                description="Choose if search only in transcripts",
                required=False,
                type=int,
                default=0,
            ),
        ],
    ),
)
class PlaylistViewSet(DefaultModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Playlist.objects.for_viewset().order_by("-created")
    serializer_class = PlaylistRetrieveSerializer
    serializer_action_classes = {
        "create": PlaylistCreateSerializer,
        "update": PlaylistUpdateSerializer,
        "partial_update": PlaylistUpdateSerializer,
        "add_video": PlaylistVideoSerializer,
        "remove_video": PlaylistVideoDeleteSerializer,
        "interact": InteractionsCreateSerializer,
        "my": PlaylistRetrieveSerializer,
        "full_search": None,
        "suggest_video": SuggestVideoSerializer,
        "generate": PlaylistGenerateSerializer,
        "expenses_report": TotalExpensesReportSerializer,
        "retrieve_expenses_report": ExpensesReportDetailSerializer,
    }
    lookup_field = "public_id"
    filterset_class = PlaylistsFilterset

    def get_queryset(self) -> QuerySet[Playlist]:
        if self.action == "list":
            return (
                Playlist.objects.for_viewset()
                .exclude(
                    privacy_type__in=[Playlist.PrivacyTypeChoices.PRIVATE, Playlist.PrivacyTypeChoices.COMMERCIAL],
                )
                .order_by("-created")
            )
        return self.queryset

    def perform_create(self: t.Self, serializer: PlaylistCreateSerializer) -> Playlist:  # type: ignore[override]
        return PlaylistCreator(**serializer.validated_data, owner=self.request.user)()

    def perform_update(self: t.Self, serializer: PlaylistUpdateSerializer) -> Playlist:  # type: ignore[override]
        return PlaylistUpdater(serializer=serializer, instance=self.get_object(), user=self.request.user)()

    def get_object(self) -> Playlist:
        return get_object_or_404(self.get_queryset(), pk=self.kwargs.get("public_id"))

    @action(detail=True, methods=["post"], url_path="add-video", permission_classes=[IsPlaylistOwner])
    def add_video(self, request: Request, *args: t.Any, **kwargs: t.Any) -> Response:
        serializer = self.get_serializer(data=self.request.data)
        PlaylistVideoAdder(playlist=self.get_object(), serializer=serializer, user=self.request.user)()

        return Response(PlaylistRetrieveSerializer(self.get_object()).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"], url_path="remove-video", permission_classes=[IsPlaylistOwner])
    def remove_video(self, request: Request, *args: t.Any, **kwargs: t.Any) -> Response:
        playlist = self.get_object()
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        playlist.videos.remove(self.video)
        playlist.remove_video_from_list_ai_suggested(self.video.pk)
        playlist.refresh_from_db()

        return Response(PlaylistRetrieveSerializer(playlist).data, status=status.HTTP_200_OK)

    @property
    def video(self) -> Video:
        try:
            video_qs = Video.objects.filter(pk=UUID(self.request.data.get("video_public_id")))
            if not video_qs.exists():
                raise NotFound("Video with such public id does not exist")

            return video_qs.first()
        except ValueError as err:
            raise ValidationError("Invalid video public id") from err

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def my(self, request: Request, *args: t.Any, **kwargs: t.Any) -> Response:
        qs = Playlist.objects.for_viewset().order_by("-created").for_user(self.request.user)

        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"], permission_classes=[AllowAny], url_path="full_search", url_name="full_search")
    def search(self, request: Request, *args: t.Any, **kwargs: t.Any) -> Response:
        playlist = self.get_object()
        results = Searcher(
            query=self.request.query_params.get("query", ""),
            only_transcripts=self.request.query_params.get("only_transcripts", 0),
            playlist=playlist,
        )()

        return Response(data=Formatter(ai_results=results.get("results"))())

    @action(
        detail=False,
        methods=["get"],
        permission_classes=[IsAuthenticated],
        url_path="expenses-report",
        url_name="get-expenses-reports",
    )
    def expenses_report(self, request: Request, *args: t.Any, **kwargs: t.Any) -> Response:
        qs = (
            GPTExpensesReport.objects.filter(user=self.request.user)
            .values("playlist")
            .annotate(
                total_units=Sum("units_spent"),
            )
            .order_by()
        )

        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(
        detail=True,
        methods=["get"],
        permission_classes=[IsAuthenticated],
        url_path="expenses-report",
        url_name="retrieve-expenses-reports",
    )
    def retrieve_expenses_report(self, request: Request, *args: t.Any, **kwargs: t.Any) -> Response:
        playlist = self.get_object()
        qs = GPTExpensesReport.objects.filter(
            playlist=playlist,
            user=self.request.user,
        ).order_by("-created")

        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)


class CategoryViewSet(ReadonlyModelViewSet):
    permission_classes = [AllowAny]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
