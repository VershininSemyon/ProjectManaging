
from rest_framework.throttling import AnonRateThrottle


class ProjectRateThrottle(AnonRateThrottle):
    scope = 'projects'


class TeamRateThrottle(AnonRateThrottle):
    scope = 'teams'


class TaskRateThrottle(AnonRateThrottle):
    scope = 'tasks'
