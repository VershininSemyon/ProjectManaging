
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

from .views import ProjectViewSet, TaskViewSet, TeamViewSet


router = DefaultRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'teams', TeamViewSet)
router.register(r'tasks', TaskViewSet)


projects_router = routers.NestedDefaultRouter(router, r'projects', lookup='project')
projects_router.register(r'teams', TeamViewSet, basename='project-teams')

teams_router = routers.NestedDefaultRouter(projects_router, r'teams', lookup='team')
teams_router.register(r'tasks', TaskViewSet, basename='team-tasks')


urlpatterns = [
    path('', include(router.urls)),
    path('', include(projects_router.urls)),
    path('', include(teams_router.urls))
]
