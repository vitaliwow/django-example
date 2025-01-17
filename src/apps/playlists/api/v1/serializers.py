from typing import Any

from rest_framework import serializers
from rest_framework.serializers import BooleanField, ModelSerializer, Serializer, UUIDField
from rest_framework.validators import UniqueValidator

from apps.playlists.api.v1.base_serializers import BaseTokenSerializer
from apps.playlists.models import Category, GPTExpensesReport, Playlist
from apps.users.models import User
from apps.videos.models import Video


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "public_id",
            "name",
            "image",
        ]


class VideoSerializer(ModelSerializer):
    class Meta:
        model = Video
        fields = [
            "public_id",
        ]


class VideoPlaylistSerializer(ModelSerializer):
    class Meta:
        model = Video
        fields = [
            "public_id",
            "title",
            "thumbnail_url",
        ]


class PlaylistVideoAddSerializer(Serializer):
    video_public_id = serializers.UUIDField(required=True)
    is_ai_suggested = serializers.BooleanField(default=False)


class PlaylistVideoSerializer(Serializer):
    videos = PlaylistVideoAddSerializer(required=True, many=True)


class PlaylistVideoDeleteSerializer(Serializer):
    video_public_id = UUIDField(required=True)


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            "public_id",
            "avatar",
            "username",
        ]


class PlaylistRetrieveSerializer(ModelSerializer):
    category = CategorySerializer()
    videos = VideoPlaylistSerializer(read_only=True, many=True)
    owner = UserSerializer(read_only=True)
    quizes = serializers.PrimaryKeyRelatedField(many=True, queryset=Quiz.objects.all())

    class Meta:
        model = Playlist
        fields = [
            "public_id",
            "title",
            "description",
            "category",
            "videos",
            "availability_status",
            "privacy_type",
            "likes_count",
            "viewed_count",
            "purpose",
            "owner",
            "list_ai_suggested_video_pks",
            "quizes",
        ]


class PlaylistCreateSerializer(ModelSerializer):
    title = serializers.CharField(
        validators=[UniqueValidator(queryset=Playlist.objects.all())],
    )

    class Meta:
        model = Playlist
        fields = [
            "title",
            "description",
            "category",
            "privacy_type",
            "purpose",
        ]


class PlaylistUpdateSerializer(ModelSerializer):
    class Meta:
        model = Playlist
        fields = [
            "title",
            "description",
            "category",
            "privacy_type",
            "users",
            "availability_status",
            "purpose",
        ]


class InteractionsCreateSerializer(Serializer):
    is_liked = BooleanField(required=False)
    is_viewed = BooleanField(required=False)


class InteractionsRetrieveSerializer(ModelSerializer):
    class Meta:
        model = PlaylistInteraction
        fields = [
            "publicId",
            "is_liked",
            "is_viewed",
            "playlist",
            "user",
        ]


class SuggestVideoSerializer(serializers.Serializer):
    previously_suggested_videos = serializers.ListField(child=serializers.UUIDField(), required=False)


class PlaylistGenerateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=150, required=False)


class VideoSuggestSerializer(ModelSerializer):
    class Meta:
        model = Video
        fields = [
            "public_id",
            "title",
            "thumbnail_url",
        ]


class PrivateLinkSerializer(BaseTokenSerializer):
    def validate_token(self, token: str) -> dict[str, Any]:
        return super().validate_token(token)


class ExpensesReportDetailSerializer(ModelSerializer):
    playlist = serializers.ReadOnlyField(source="playlists.public_id")

    class Meta:
        model = GPTExpensesReport
        fields = (
            "public_id",
            "type_operation",
            "playlist",
            "units_spent",
            "api_request",
        )


class TotalExpensesReportSerializer(ModelSerializer):
    total_units = serializers.IntegerField(read_only=True)  # annotated
    playlist = serializers.UUIDField(format="hex_verbose")

    class Meta:
        model = GPTExpensesReport
        fields = (
            "playlist",
            "total_units",
        )
