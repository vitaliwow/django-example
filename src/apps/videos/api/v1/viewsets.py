import typing as t

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from apps.ai_integration.services.searcher import Searcher
from apps.ai_integration.services.formatter import Formatter
from apps.videos.api.v1.filtersets import VideoFilterset
from apps.videos.api.v1.mixins import AccessForStaffMixin
from apps.videos.api.v1.permissions import SpecialUserPermission
from apps.videos.api.v1.serializers import (
    VideoCreateSerializer,
    VideoFileCreateSerializer,
    VideoFileRetrieveSerializer,
    VideoRetrieveSerializer,
    VideoUpdateSerializer, FileS3Serializer,
)
from apps.videos.helpers import extract_file_name_from_link
from apps.videos.models import Video, VideoFile
from apps.videos.services.video.creators import VideoCreateManager
from apps.videos.services.video.creators.video_file import VideoFileCreator
from apps.videos.services.video.creators.video_from_videofile import VideoFromVideoFileCreator
from apps.videos.services.video.video_deleter import VideoDeleter
from apps.videos.services.video.video_updater import VideoUpdater
from apps.videos.tasks import get_raw_transcript
from apps.videos.tasks.download_file_s3 import update_video_file_from_storage
from core.api.viewsets import (
    BaseGenericViewSet,
    CreateReadDeleteModelViewSet,
    DefaultModelViewSet,
)
from core.conf.environ import env


class VideoViewSet(DefaultModelViewSet):
    permission_classes = (AllowAny,)
    queryset = Video.objects.for_viewset()
    serializer_class = VideoRetrieveSerializer
    serializer_action_classes = {
        "create": VideoCreateSerializer,
        "update": VideoUpdateSerializer,
        "partial_update": VideoUpdateSerializer,
        "my": VideoRetrieveSerializer,
    }
    lookup_field = "public_id"
    filterset_class = VideoFilterset
    
    def get_queryset(self):
        return self.queryset

    def perform_create(self: t.Self, serializer: VideoCreateSerializer) -> Video:  # type: ignore[override]
        return VideoCreateManager(data=serializer.validated_data, user=self.request.user)()

    def perform_update(self: t.Self, serializer: VideoUpdateSerializer) -> Video:  # type: ignore[override]
        return VideoUpdater(data=serializer.validated_data, instance=self.get_object(), user=self.request.user)()

    def perform_destroy(self, instance: Video) -> None:
        VideoDeleter(video=instance, user=self.request.user)()

    def get_object(self) -> Video:
        obj: Video| None = self.get_queryset().filter(pk=self.kwargs.get("public_id")).first()
        if obj is None:
            raise NotFound("Video not found")
        return obj

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def my(self, request: Request, *args: t.Any, **kwargs: t.Any) -> Response:
        qs = self.get_queryset().for_user(self.request.user)
        
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"], permission_classes=[AllowAny])
    def full_search(self, request: Request, *args: t.Any, **kwargs: t.Any) -> Response:
        video_id = kwargs.get('public_id')

        results = Searcher(
            query=self.request.query_params.get("query", ""),
            only_transcripts=self.request.query_params.get("only_transcripts", 0),
            video_id=video_id
        )()

        return Response(data=Formatter(ai_results=results.get("results"))())

    if env("SERVER_TYPE") == "test":

        @action(detail=False, methods=["get"], permission_classes=[AllowAny])
        def get_transcript(self, request: Request, *args: t.Any, **kwargs: t.Any) -> Response:
            video_id = request.query_params.get("video_id")
            if not video_id:
                return Response({"error": "video_id is required"}, status=400)
            transcript = get_raw_transcript(video_id)
            return Response(transcript)


class VideoFileDownloadViewSet(AccessForStaffMixin, CreateReadDeleteModelViewSet):
    """Views to create, read, delete transcripts and its chunks (cues)"""

    permission_classes = (SpecialUserPermission,)
    queryset = VideoFile.objects.prefetch_related("user")
    serializer_class = VideoFileRetrieveSerializer
    serializer_action_classes = {
        "create": VideoFileCreateSerializer,
        "retrieve": VideoFileRetrieveSerializer,
        "list": VideoFileRetrieveSerializer,
        "delete": VideoFileRetrieveSerializer,
        "create_materials": None,
    }
    lookup_field = "public_id"

    def perform_create(self: BaseGenericViewSet, serializer: VideoFileRetrieveSerializer) -> VideoFile:
        return VideoFileCreator(serializer.validated_data, user=self.request.user)()

    def perform_destroy(self, instance: VideoFile) -> None:
        instance: VideoFile = self.get_object()
        instance.file.delete()
        instance.ogg.delete()
        instance.delete()

    @extend_schema(request=FileS3Serializer, responses={status.HTTP_201_CREATED: None})
    @action(methods=["post"], url_path="file-s3", detail=False)
    def create_from_storage(self, request: Request, *args: t.Any, **kwargs: dict[str, t.Any]) -> Response:
        """Create a video file from the given link

        Expected link format: https://storage.yandexcloud.net/{bucket_id}/{object_id}
        """
        response = Response(status=status.HTTP_201_CREATED)
        if link := request.data.get("link"):
            video_file = VideoFile.objects.create(user=self.request.user)
            video = VideoFromVideoFileCreator(
                video_file=video_file,
                user=self.request.user,
                title=extract_file_name_from_link(link),
                link=link,
            )()

            update_video_file_from_storage.delay(link, video_file_pk=video_file.pk)
            response.data = {"publicId": video.pk}
        return response
