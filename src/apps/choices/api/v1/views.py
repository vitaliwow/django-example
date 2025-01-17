import typing as t

from rest_framework.response import Response
from rest_framework.views import APIView

from core.models.choices import PurposeChoices


class PurposeAPIView(APIView):
    def get(self, *args: t.Any, **kwargs: dict) -> Response:
        return Response(data=dict(PurposeChoices.choices))
