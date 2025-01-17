from rest_framework.pagination import PageNumberPagination

from core.conf import api


class AppPagination(PageNumberPagination):
    page_size_query_param = "page_size"
    max_page_size = api.MAX_PAGE_SIZE
