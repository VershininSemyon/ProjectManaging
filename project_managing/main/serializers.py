
from rest_framework import serializers

from .models import Project, Task, Team


class ProjectSerializer(serializers.ModelSerializer):
    creator_username = serializers.CharField(source='creator.username', read_only=True)
    creator_email = serializers.CharField(source='creator.email', read_only=True)

    teams_count = serializers.SerializerMethodField(method_name='get_teams_count')

    def get_teams_count(self, obj):
        return obj.teams.count()

    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ('id', 'created_at', )


class TeamSerializer(serializers.ModelSerializer):
    project_title = serializers.CharField(source='project.title', read_only=True)

    members_count = serializers.SerializerMethodField(method_name='get_members_count')
    tasks_count = serializers.SerializerMethodField(method_name='get_tasks_count')

    def get_members_count(self, obj):
        return obj.members.count()

    def get_tasks_count(self, obj):
        return obj.tasks.count()

    class Meta:
        model = Team
        fields = '__all__'
        read_only_fields = ('id', 'created_at', )


class TaskSerializer(serializers.ModelSerializer):
    project_title = serializers.CharField(source='team.project.title', read_only=True)
    team_title = serializers.CharField(source='team.title', read_only=True)

    assignee_count = serializers.SerializerMethodField(method_name='get_assignee_count')

    def get_assignee_count(self, obj):
        return obj.assignee.count()

    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ('id', 'created_at', )
