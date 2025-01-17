import requests
from django.conf import settings
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.permissions import IsCommercialUser


class PreSignedUrlS3APIView(APIView):
    permission_classes = (IsCommercialUser,)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="file_type",
                location=OpenApiParameter.QUERY,
                required=True,
                type=str,
            ),
            OpenApiParameter(
                name="file_name",
                location=OpenApiParameter.QUERY,
                required=True,
                type=str,
            ),
        ],
    )
    def get(self, request, *args, **kwargs):
        headers = {"Authorization": f"Api-Key {settings.SA_MEDIA_UPLOADER_SECRET_KEY}"}
        params = {
            "user_id": request.user.pk,
            "file_type": request.query_params["file_type"],
            "file_name": request.query_params["file_name"],
        }
        response = requests.get(
            f"https://functions.yandexcloud.net/{settings.CF_MEDIA_UPLOADER}",
            headers=headers,
            params=params,
            timeout=30,
        ).json()

        return Response(response, status=status.HTTP_200_OK)
