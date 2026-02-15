
from rest_framework.pagination import PageNumberPagination


class ProjectPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = "project_page_size"


class TeamPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = "team_page_size"


class TaskPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = "task_page_size"
