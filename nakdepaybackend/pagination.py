from rest_framework.pagination import PageNumberPagination
from collections import OrderedDict
from rest_framework.response import Response


class CustomResultsSetPagination(PageNumberPagination):
    """
    create class CustomResultsSetPagination from PageNumberPagination to give us
    full control to create custom Pagination to every needed class
    """
    page_size = 10
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        return {
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'limit': int(self.request.query_params.get(self.page_size_query_param,
                                                       self.page_size)),
            'data': data
        }


class CustomResultsSetPagination1(PageNumberPagination):
    """
    create class CustomResultsSetPagination from PageNumberPagination to give us
    full control to create custom Pagination to every needed class
    """
    page_size = 10
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'limit': int(self.request.query_params.get(self.page_size_query_param,
                                                       self.page_size)),
            'data': data
        })