
from django.db import models
from users.models import User


class Project(models.Model):
    title = models.CharField(max_length=300, unique=True)
    description = models.TextField(blank=True, null=True)
    is_private = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    creator = models.ForeignKey(to=User, related_name='created_projects', on_delete=models.CASCADE)

    def __str__(self):
        return f"Project {self.title} by {self.creator}"


class Team(models.Model):
    title = models.CharField(max_length=100)
    project = models.ForeignKey(to=Project, related_name='teams', on_delete=models.CASCADE)
    members = models.ManyToManyField(to=User, related_name='teams_take_part', blank=True)

    def __str__(self):
        return f"Team {self.title} in project {self.project.title}"


class Task(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    assignee = models.ManyToManyField(to=User, related_name='assigned_tasks', blank=True)
    team = models.ForeignKey(to=Team, related_name='tasks', on_delete=models.CASCADE)

    deadline = models.DateTimeField()

    class TaskStatus(models.TextChoices):
        IN_PROCESS = 'in_process', 'В процессе'
        DONE = 'done', 'Выполнена'
        CANCELLED = 'cancelled', 'Отменена'
    
    status = models.CharField(max_length=12, choices=TaskStatus.choices)

    def __str__(self):
        return f"Task {self.title} in team {self.team.title}"
