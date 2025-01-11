from rest_framework import pagination


class SimplePagination(pagination.PageNumberPagination):
    page_size = 12
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    max_page_size = 100