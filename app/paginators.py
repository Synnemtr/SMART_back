from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.exceptions import NotFound


class CustomPagination(PageNumberPagination):
    page_size = 18

    def paginate_queryset(self, queryset, request, view=None):
        page_number = request.query_params.get(self.page_query_param, None)
        if not page_number:
            return queryset
        else:
            try:
                return super(CustomPagination, self).paginate_queryset(
                    queryset, request, view=None
                )
            except NotFound as e:
                return queryset.model.objects.none()

    def get_paginated_response(self, data):
        return Response(data)
