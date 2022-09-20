

from rest_framework.pagination import PageNumberPagination,CursorPagination


class StandardPagination(CursorPagination):
    ordering='-created_date'


class StandardcommentPagination(CursorPagination):
    ordering='-created_on'

