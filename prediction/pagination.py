from rest_framework import pagination


class LargeResultsSetPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    page_query_param = "page_no"
    max_page_size = 100
