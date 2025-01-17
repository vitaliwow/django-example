__all__ = [
    "CreateOnlyModelViewSet",
    "CreateAndReadModelViewSet",
    "CreateListModelViewSet",
    "CreateUpdateModelViewSet",
    "CreateReadDeleteModelViewSet",
    "DefaultModelViewSet",
    "ListModelViewSet",
    "ListRetrieveUpdateModelViewSet",
    "ListUpdateModelViewSet",
    "ReadonlyModelViewSet",
    "RetrieveOnlyModelViewSet",
    "WithoutDeleteModelViewSet",
    "WithoutListModelViewSet",
    "WithoutUpdateModelViewSet",
    "BaseSerializer",
    "BaseGenericViewSet",
    "RetrieveUpdateModelViewSet",
    "WithoutCreateModelViewSet",

    "ListUpdateDeleteModelViewSet",
    "MaterialsViewSet",
]

import typing as t

from django.db.models import QuerySet
from rest_framework import mixins, permissions, status
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer
from rest_framework.viewsets import GenericViewSet

from apps.users.models import User


class AuthenticatedRequest(Request):
    user: User


class BaseGenericViewSet(t.Protocol):
    request: AuthenticatedRequest

    def get_serializer(self, *args: t.Any, **kwargs: t.Any) -> t.Any:
        ...

    def get_response(self, *args: t.Any, **kwargs: t.Any) -> t.Any:
        ...

    def perform_create(self, *args: t.Any, **kwargs: t.Any) -> t.Any:
        ...

    def perform_update(self, *args: t.Any, **kwargs: t.Any) -> t.Any:
        ...

    def get_success_headers(self, *args: t.Any, **kwargs: t.Any) -> t.Any:
        ...

    def get_serializer_class(self, *args: t.Any, **kwargs: t.Any) -> t.Any:
        ...

    def get_object(self, *args: t.Any, **kwargs: t.Any) -> t.Any:
        ...


class AuthenticatedGenericViewSet(GenericViewSet):
    request: AuthenticatedRequest
    permission_classes = [permissions.IsAuthenticated]


class DefaultCreateModelMixin(CreateModelMixin):
    """Return detail-serialized created instance"""

    def create(self: BaseGenericViewSet, request: Request, *args: t.Any, **kwargs: t.Any) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)  # No getting created instance in original DRF
        headers = self.get_success_headers(serializer.data)
        return self.get_response(instance, status.HTTP_201_CREATED, headers)

    def perform_create(self: BaseGenericViewSet, serializer: t.Any) -> t.Any:
        return serializer.save()  # No returning created instance in original DRF


class DefaultUpdateModelMixin(UpdateModelMixin):
    """Return detail-serialized updated instance"""

    def update(self: BaseGenericViewSet, request: Request, *args: t.Any, **kwargs: t.Any) -> Response:
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_update(serializer)  # No getting updated instance in original DRF
        response = self.get_response(instance, status.HTTP_200_OK)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}  # noqa:SLF001

        return response

    def perform_update(self: BaseGenericViewSet, serializer: t.Any) -> t.Any:
        return serializer.save()  # No returning updated instance in original DRF


class ResponseWithRetrieveSerializerMixin:
    """
    Always response with 'retrieve' serializer or fallback to `serializer_class`.
    Usage:

    class MyViewSet(DefaultModelViewSet):
        serializer_class = MyDefaultSerializer
        serializer_action_classes = {
           'list': MyListSerializer,
           'my_action': MyActionSerializer,
        }
        @action
        def my_action:
            ...

    'my_action' request will be validated with MyActionSerializer,
    but response will be serialized with MyDefaultSerializer
    (or 'retrieve' if provided).

    Thanks gonz: http://stackoverflow.com/a/22922156/11440

    """

    def get_response(self: BaseGenericViewSet, instance: t.Any, status: t.Any, headers: t.Any = None) -> Response:
        retrieve_serializer_class = self.get_serializer_class(action="retrieve")
        context = self.get_serializer_context()  # type: ignore
        retrieve_serializer = retrieve_serializer_class(instance, context=context)
        return Response(retrieve_serializer.data, status=status, headers=headers)

    def get_serializer_class(self: BaseGenericViewSet, action: str | None = None) -> type[BaseSerializer]:
        if action is None:
            action = self.action  # type: ignore

        try:
            return self.serializer_action_classes[action]  # type: ignore
        except (KeyError, AttributeError):
            return super().get_serializer_class()


class DefaultModelViewSet(
    DefaultCreateModelMixin,  # Create response is overriden
    mixins.RetrieveModelMixin,
    DefaultUpdateModelMixin,  # Update response is overriden
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    ResponseWithRetrieveSerializerMixin,  # Response with retrieve or default serializer
    AuthenticatedGenericViewSet,
):
    pass


class CreateOnlyModelViewSet(
    DefaultCreateModelMixin,
    ResponseWithRetrieveSerializerMixin,
    AuthenticatedGenericViewSet,
):
    pass


class CreateUpdateModelViewSet(
    DefaultCreateModelMixin,
    DefaultUpdateModelMixin,
    ResponseWithRetrieveSerializerMixin,
    AuthenticatedGenericViewSet,
):
    pass


class WithoutListModelViewSet(
    DefaultCreateModelMixin,
    mixins.RetrieveModelMixin,
    DefaultUpdateModelMixin,
    mixins.DestroyModelMixin,
    ResponseWithRetrieveSerializerMixin,
    AuthenticatedGenericViewSet,
):
    """Default ViewSet but without list."""


class WithoutDeleteModelViewSet(
    DefaultCreateModelMixin,  # Create response is overriden
    mixins.RetrieveModelMixin,
    DefaultUpdateModelMixin,  # Update response is overriden
    mixins.ListModelMixin,
    ResponseWithRetrieveSerializerMixin,  # Response with retrieve or default serializer
    AuthenticatedGenericViewSet,
):
    pass


class WithoutUpdateModelViewSet(
    DefaultCreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    ResponseWithRetrieveSerializerMixin,
    AuthenticatedGenericViewSet,
):
    pass


class ReadonlyModelViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    ResponseWithRetrieveSerializerMixin,  # Response with retrieve or default serializer
    AuthenticatedGenericViewSet,
):
    pass


class RetrieveOnlyModelViewSet(
    mixins.RetrieveModelMixin,
    ResponseWithRetrieveSerializerMixin,  # Response with retrieve or default serializer
    AuthenticatedGenericViewSet,
):
    pass


class ListModelViewSet(mixins.ListModelMixin, GenericViewSet):
    pass


class ListRetrieveUpdateModelViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    DefaultUpdateModelMixin,
    ResponseWithRetrieveSerializerMixin,
    AuthenticatedGenericViewSet,
):
    pass


class ListUpdateModelViewSet(
    DefaultUpdateModelMixin,
    mixins.ListModelMixin,
    ResponseWithRetrieveSerializerMixin,
    AuthenticatedGenericViewSet,
):
    pass


class RetrieveUpdateModelViewSet(
    mixins.RetrieveModelMixin,
    DefaultUpdateModelMixin,
    ResponseWithRetrieveSerializerMixin,
    AuthenticatedGenericViewSet,
):
    pass


class UpdateOnlyModelViewSet(
    DefaultUpdateModelMixin,
    ResponseWithRetrieveSerializerMixin,
    AuthenticatedGenericViewSet,
):
    pass


class CreateAndReadModelViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    CreateOnlyModelViewSet,
):
    pass


class CreateListModelViewSet(
    mixins.ListModelMixin,
    CreateOnlyModelViewSet,
):
    pass


class WithoutCreateModelViewSet(
    mixins.RetrieveModelMixin,
    DefaultUpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    ResponseWithRetrieveSerializerMixin,
    AuthenticatedGenericViewSet,
):
    pass


class CreateReadDeleteModelViewSet(
    DefaultCreateModelMixin,  # Create response is overriden
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    ResponseWithRetrieveSerializerMixin,  # Response with retrieve or default serializer
    GenericViewSet,
):
    request: AuthenticatedRequest


class ListUpdateDeleteModelViewSet(
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    DefaultUpdateModelMixin,
    ResponseWithRetrieveSerializerMixin,
    AuthenticatedGenericViewSet,
):
    pass


class MaterialsViewSet(ListUpdateDeleteModelViewSet):
    lookup_field = "public_id"

    def get_queryset(self) -> QuerySet:
        return self.queryset.filter(video__pk=self.kwargs.get("video_pk"))
