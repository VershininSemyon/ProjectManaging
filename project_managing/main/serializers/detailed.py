
from .common import ProjectSerializer, TeamSerializer, TaskSerializer, MemberSerializer


class DetailProjectSerializer(ProjectSerializer):
    teams = TeamSerializer(many=True, read_only=True)


class DetailTeamSerializer(TeamSerializer):
    project = ProjectSerializer(read_only=True)
    tasks = TaskSerializer(read_only=True, many=True)
    members = MemberSerializer(read_only=True, many=True)


class DetailTaskSerializer(TaskSerializer):
    team = TeamSerializer(read_only=True)
    assignee = MemberSerializer(read_only=True, many=True)


class DetailMemberSerializer(MemberSerializer):
    team = TeamSerializer(read_only=True)
