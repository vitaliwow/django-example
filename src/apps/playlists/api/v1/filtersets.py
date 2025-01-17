from django_filters import rest_framework as filters


class PlaylistsFilterset(filters.FilterSet):
    title = filters.CharFilter(field_name="title", lookup_expr="icontains")
    description = filters.CharFilter(field_name="description", lookup_expr="icontains")
    video_title = filters.CharFilter(field_name="videos__title", lookup_expr="icontains")
    video_description = filters.CharFilter(field_name="videos__description", lookup_expr="icontains")
