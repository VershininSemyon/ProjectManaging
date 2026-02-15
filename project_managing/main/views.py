
from django.core.cache import cache
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from .filters import ProjectFilter, TaskFilter, TeamFilter
from .models import Project, Task, Team
from .paginations import ProjectPagination, TaskPagination, TeamPagination
from .permissions import *
from .serializers import ProjectSerializer, TaskSerializer, TeamSerializer
from .tasks import (send_project_created_notification,
                    send_project_deleted_notification)


class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = []

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter
    ]

    filterset_class = ProjectFilter
    search_fields = [
        'title',
        'description'
    ]
    ordering_fields = [
        'title',
        'created_at',
        'is_private'
    ]

    pagination_class = ProjectPagination
    throttle_scope = "projects"

    def create(self, request, *args, **kwargs):
        result = super().create(request, *args, **kwargs)

        if result.status_code == 201:
            project_id = result.data['id']
            project_title = result.data['title']
            user_email = request.user.email

            send_project_created_notification.delay(project_id, project_title, user_email)

        return result
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        project_id = instance.id
        project_title = instance.title
        user_email = request.user.email
        
        result = super().destroy(request, *args, **kwargs)
        if result.status_code == 204:
            send_project_deleted_notification.delay(project_id, project_title, user_email)

        return result


class TeamViewSet(ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = []

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter
    ]

    filterset_class = TeamFilter
    search_fields = [
        'title',
    ]
    ordering_fields = [
        'title',
        'project__title',
        'project__created_at'
    ]

    pagination_class = TeamPagination
    throttle_scope = "teams"

    def get_queryset(self):
        if 'project_pk' in self.kwargs:
            return Team.objects.filter(project_id=self.kwargs['project_pk'])
        return super().get_queryset()
    
    def perform_create(self, serializer):
        if 'project_pk' in self.kwargs:
            serializer.save(project_id=self.kwargs['project_pk'])
        else:
            serializer.save()


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = []

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter
    ]

    filterset_class = TaskFilter
    search_fields = [
        'title',
        'description',
    ]
    ordering_fields = [
        'title',
        'created_at',
        'deadline',
        'status',
    ]

    pagination_class = TaskPagination
    throttle_scope = "tasks"

    def get_queryset(self):
        if 'team_pk' in self.kwargs:
            return Task.objects.filter(team_id=self.kwargs['team_pk'])
        return super().get_queryset()
    
    def perform_create(self, serializer):
        if 'team_pk' in self.kwargs:
            serializer.save(team_id=self.kwargs['team_pk'])
        else:
            serializer.save()
