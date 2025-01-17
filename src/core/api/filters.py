from django_filters import BaseInFilter, BaseRangeFilter
from django_filters import rest_framework as filters


class CharInFilter(BaseInFilter, filters.CharFilter):
    pass


class NumberRangeFilter(BaseRangeFilter, filters.NumberFilter):
    pass
