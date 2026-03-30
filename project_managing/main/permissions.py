
from rest_framework import permissions
from users.models import User
from django.shortcuts import get_object_or_404
from .models import Project, Team, Task, Member


def is_project_creator(user, project):
    return user == project.creator

def is_project_member(user, project):
    return Member.objects.filter(
        user=user,
        team__project=project
    ).exists()

def has_role_in_team(user, team, role):
    return Member.objects.filter(
        user=user,
        team=team,
        role_type=role
    ).exists()

def is_task_assignee(user, task):
    return task.assignee.filter(user=user).exists()

def get_user_role_in_team(user, team):
    try:
        member = Member.objects.get(user=user, team=team)
        return member.role_type
    except Member.DoesNotExist:
        return None

def can_change_role(from_role, to_role):
    role_order = {
        Member.RoleTypes.PARTICIPANT: 1,
        Member.RoleTypes.MODERATOR: 2,
        Member.RoleTypes.ADMINISTRATOR: 3
    }
    return role_order.get(from_role, 0) > role_order.get(to_role, 999)

def is_team_member(user, team):
    return Member.objects.filter(user=user, team=team).exists()


class ProjectPermission(permissions.IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        # Просмотр: публичные видят все, приватные - только участники
        if request.method in permissions.SAFE_METHODS:
            if not obj.is_private:
                return True
            return is_project_member(request.user, obj)
        
        # Изменение/удаление: только создатель
        return is_project_creator(request.user, obj)


class TeamPermission(permissions.IsAuthenticatedOrReadOnly):
    def has_permission(self, request, view):
        if hasattr(view, 'kwargs') and 'project_pk' in view.kwargs:
            project_id = view.kwargs['project_pk']
            project = get_object_or_404(Project, id=project_id)

        # Просмотр списка команд: создатель и участники проекта
        if request.method in permissions.SAFE_METHODS:
            return is_project_member(request.user, project) or is_project_creator(request.user, project)

        # Создание команды: только создатель проекта
        return is_project_creator(request.user, project)

    def has_object_permission(self, request, view, obj):
        # Просмотр команды: создатель и участники проекта
        if request.method in permissions.SAFE_METHODS:
            return is_project_member(request.user, obj.project) or is_project_creator(request.user, obj.project)
        
        # Редактирование: создатель проекта или администратор команды
        if request.method in ('PATCH', 'PUT'):
            return is_project_creator(request.user, obj.project) or has_role_in_team(request.user, obj, Member.RoleTypes.ADMINISTRATOR)
        
        # Удаление: только создатель проекта
        if request.method == 'DELETE':
            return is_project_creator(request.user, obj.project)
    
        return False


class MemberPermission(permissions.IsAuthenticatedOrReadOnly):
    def has_permission(self, request, view):
        if hasattr(view, 'kwargs') and 'team_pk' in view.kwargs:
            team = get_object_or_404(Team, id=view.kwargs['team_pk'])
            project = team.project
            
            # Добавление участников: создатель, админ или модератор команды
            if request.method == 'POST':
                return (
                    is_project_creator(request.user, project) or 
                    has_role_in_team(request.user, team, Member.RoleTypes.ADMINISTRATOR) or
                    has_role_in_team(request.user, team, Member.RoleTypes.MODERATOR)
                )
            
            # Просмотр списка: участники команды
            return is_team_member(request.user, team)
        
        return False

    def has_object_permission(self, request, view, obj):
        team = obj.team
        project = team.project
        user_role = get_user_role_in_team(request.user, team)
        
        # Просмотр участника: участники команды
        if request.method in permissions.SAFE_METHODS:
            return is_team_member(request.user, team)
        
        # Изменение роли участника
        if request.method in ('PATCH', 'PUT'):
            if is_project_creator(request.user, project):
                return True
            
            # Администратор может менять только на роль ниже своей
            if has_role_in_team(request.user, team, Member.RoleTypes.ADMINISTRATOR):
                target_role = request.data.get('role_type', obj.role_type)
                return can_change_role(user_role, target_role)
            
            return False
        
        # Удаление участника
        if request.method == 'DELETE':
            if is_project_creator(request.user, project):
                return True
            if has_role_in_team(request.user, team, Member.RoleTypes.ADMINISTRATOR):
                return True

            # Сам участник может выйти из команды
            return request.user == obj.user
        
        return False


class TaskPermission(permissions.IsAuthenticatedOrReadOnly):
    def has_permission(self, request, view):
        if hasattr(view, 'kwargs') and 'team_pk' in view.kwargs:
            team = get_object_or_404(Team, id=view.kwargs['team_pk'])
            project = team.project
            
            # Создание задачи: участники проекта
            if request.method == 'POST':
                return is_project_member(request.user, project)
            
            # Просмотр списка: участники команды
            return is_team_member(request.user, team)
        
        return False

    def has_object_permission(self, request, view, obj):
        team = obj.team
        project = team.project
        
        # Просмотр задачи: участники команды
        if request.method in permissions.SAFE_METHODS:
            return is_team_member(request.user, team)
        
        user_role = get_user_role_in_team(request.user, team)
        is_assignee = is_task_assignee(request.user, obj)
        
        # Редактирование задачи
        if request.method in ('PATCH', 'PUT'):
            # Исполнители могут менять только статус
            if is_assignee:
                allowed_fields = {'status'}
                if set(request.data.keys()).issubset(allowed_fields):
                    return True
            
            # Полное редактирование: создатель проекта, админ или модератор
            return (
                is_project_creator(request.user, project) or
                has_role_in_team(request.user, team, Member.RoleTypes.ADMINISTRATOR) or
                has_role_in_team(request.user, team, Member.RoleTypes.MODERATOR)
            )
        
        # Удаление задачи: создатель проекта или администратор
        if request.method == 'DELETE':
            return (
                is_project_creator(request.user, project) or
                has_role_in_team(request.user, team, Member.RoleTypes.ADMINISTRATOR)
            )
        
        return False
