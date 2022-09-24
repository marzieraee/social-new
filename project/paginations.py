

from rest_framework.pagination import PageNumberPagination,CursorPagination


class StandardPagination(PageNumberPagination):
    ordering='-created_date'


class StandardcommentPagination(PageNumberPagination):
    ordering='-created_on'

