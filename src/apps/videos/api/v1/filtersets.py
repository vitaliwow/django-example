from django_filters import rest_framework as filters


class VideoFilterset(filters.FilterSet):
    title = filters.CharFilter(field_name="title", lookup_expr="icontains")
    description = filters.CharFilter(field_name="description", lookup_expr="icontains")
