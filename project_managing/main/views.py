
from django.core.cache import cache
from django_filters.rest_framework import DjangoFilterBackend
from main.serializers.common import (MemberSerializer, ProjectSerializer,
                                     TaskSerializer, TeamSerializer)
from main.serializers.detailed import (DetailMemberSerializer,
                                       DetailProjectSerializer,
                                       DetailTaskSerializer,
                                       DetailTeamSerializer)
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from .filters import MemberFilter, ProjectFilter, TaskFilter, TeamFilter
from .models import Member, Project, Task, Team
from .paginations import (MemberPagination, ProjectPagination, TaskPagination,
                          TeamPagination)
from .permissions import *
from .tasks import (send_project_created_notification,
                    send_project_deleted_notification)


class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.prefetch_related('teams').select_related('creator')
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

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DetailProjectSerializer
        return ProjectSerializer

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
    queryset = Team.objects.prefetch_related('members', 'tasks').select_related('project')
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

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DetailTeamSerializer
        return TeamSerializer

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
    queryset = Task.objects.prefetch_related('assignee').select_related('team')
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

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DetailTaskSerializer
        return TaskSerializer

    def get_queryset(self):
        if 'team_pk' in self.kwargs:
            return Task.objects.filter(team_id=self.kwargs['team_pk'])
        return super().get_queryset()
    
    def perform_create(self, serializer):
        if 'team_pk' in self.kwargs:
            serializer.save(team_id=self.kwargs['team_pk'])
        else:
            serializer.save()


class MemberViewSet(ModelViewSet):
    queryset = Member.objects.prefetch_related('assigned_tasks').select_related('user', 'team')
    serializer_class = MemberSerializer

    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = []

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter
    ]

    filterset_class = MemberFilter
    search_fields = [
        'role_type', ''        
    ]
    ordering_fields = [
        'role_type', 'team', 'user'
    ]

    pagination_class = MemberPagination
    throttle_scope = "members"

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DetailMemberSerializer
        return MemberSerializer

    def get_queryset(self):
        if 'team_pk' in self.kwargs:
            return Member.objects.filter(team_id=self.kwargs['team_pk'])
        return super().get_queryset()
    
    def perform_create(self, serializer):
        if 'team_pk' in self.kwargs:
            serializer.save(team_id=self.kwargs['team_pk'])
        else:
            serializer.save()
