from uuid import UUID

from rest_framework import serializers

from apps.videos.models import Transcript, Video, VideoFile


class VideoRetrieveSerializer(serializers.ModelSerializer):
    quiz_ids = serializers.SerializerMethodField()
    transcription_status = serializers.SerializerMethodField()
    timecodes_status = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = ["__all__"]


class VideoCreateSerializer(serializers.Serializer):
    origin_link = serializers.CharField(required=True, max_length=250)


class VideoUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = [
            "title",
            "description",
            "starts_from",
            "purpose",
            "status",
        ]


class VideoSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = [
            "public_id",
            "title",
            "video_id",
            "starts_from",
            "created",
            "origin_link",
            "thumbnail_url",
        ]


class VideoFileRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoFile
        fields = [
            "public_id",
            "file",
            "created",
            "transcript_status",
            "summary_status",
            "short_summary_status",
            "quizz_status",
            "transcripts",
            "short_summary",
            "summary",
            "quizzes",
        ]


class VideoFileCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoFile
        fields = [
            "file",
        ]


class TranscriptRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transcript
        fields = [
            "public_id",
            "data",
        ]


class FileS3Serializer(serializers.Serializer):
    link = serializers.URLField(required=True)
