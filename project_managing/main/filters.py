
from django_filters import rest_framework as filters

from .models import Project, Team, Task


class ProjectFilter(filters.FilterSet):
    class Meta:
        model = Project
        fields = {
            'title': ['exact', 'icontains'],
            'description': ['icontains'],
            'is_private': ['exact'],
            'created_at': ['exact', 'gte', 'lte'],
            'creator': ['exact'],
            'creator__username': ['exact', 'icontains'],
            'creator__email': ['exact', 'icontains'],
        }


class TeamFilter(filters.FilterSet):
    class Meta:
        model = Team
        fields = {
            'title': ['exact', 'icontains'],
            'project': ['exact'],
            'project__title': ['exact', 'icontains'],
        }


class TaskFilter(filters.FilterSet):
    class Meta:
        model = Task
        fields = {
            'title': ['exact', 'icontains'],
            'description': ['icontains'],
            'created_at': ['exact', 'gte', 'lte'],
            'deadline': ['exact', 'gte', 'lte'],
            'status': ['exact'],
            'team': ['exact'],
            'team__title': ['exact', 'icontains'],
            'team__project': ['exact'],
            'team__project__title': ['exact', 'icontains'],
        }
