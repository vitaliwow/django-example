from django.contrib import admin
from django_object_actions import DjangoObjectActions
from django.db.models import F

from apps.videos.models import Transcript


@admin.register(Transcript)
class TranscriptAdmin(DjangoObjectActions, admin.ModelAdmin):
    list_display = ('public_id', 'video_title',)
    search_fields = ('video__title',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('video').annotate(video_title=F('video__title'))

    def video_title(self, obj):
        return obj.video_title
    video_title.admin_order_field = 'video__title'
    video_title.short_description = 'Video Title'
