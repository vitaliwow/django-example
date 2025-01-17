from django.urls import include, path
from rest_framework.routers import SimpleRouter

from . import viewsets
from .view import PreSignedUrlS3APIView

router = SimpleRouter()
router.register("videos", viewsets.VideoViewSet)
router.register("video-files", viewsets.VideoFileDownloadViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path("big-size-files/presigned-url/", PreSignedUrlS3APIView.as_view(), name="upload-file-s3"),
]
