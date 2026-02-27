
from django.db import models
from users.models import User


class Project(models.Model):
    title = models.CharField(max_length=300, unique=True)
    description = models.TextField(blank=True, null=True)
    is_private = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    creator = models.ForeignKey(to=User, related_name='created_projects', on_delete=models.CASCADE)

    def __str__(self):
        return f"Project {self.title} by user {self.creator.username}"


class Team(models.Model):
    title = models.CharField(max_length=100)
    project = models.ForeignKey(to=Project, related_name='teams', on_delete=models.CASCADE)

    def __str__(self):
        return f"Team {self.title} in project {self.project.title}"


class Member(models.Model):
    class RoleTypes(models.TextChoices):
        PARTICIPANT = 'participant', 'Участник'
        MODERATOR = 'moderator', 'Модератор'
        ADMINISTRATOR = 'administrator', 'Администратор'

    role_type = models.CharField(choices=RoleTypes.choices, max_length=13)
    user = models.ForeignKey(to=User, related_name='members', on_delete=models.CASCADE)
    team = models.ForeignKey(to=Team, related_name='members', on_delete=models.CASCADE)

    def __str__(self):
        return f"User {self.user.username} is {self.role_type} in team {self.team.title}"


class Task(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    assignee = models.ManyToManyField(to=Member, related_name='assigned_tasks')
    team = models.ForeignKey(to=Team, related_name='tasks', on_delete=models.CASCADE)

    deadline = models.DateTimeField()

    class TaskStatus(models.TextChoices):
        IN_PROCESS = 'in_process', 'В процессе'
        DONE = 'done', 'Выполнена'
        CANCELLED = 'cancelled', 'Отменена'
    
    status = models.CharField(max_length=12, choices=TaskStatus.choices)

    def __str__(self):
        return f"Task {self.title} in team {self.team.title} is in status {self.status}"
