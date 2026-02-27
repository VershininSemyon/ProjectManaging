
from django.contrib import admin

from .models import Project, Task, Team, Member


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'creator',
        'is_private',
        'created_at'
    )
    
    search_fields = (
        'title',
        'description',
        'creator__username'
    )
    
    list_filter = (
        'is_private',
        'created_at'
    )


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'project'
    )
    
    search_fields = (
        'title',
        'project__title'
    )
    
    list_filter = (
        'project',
    )


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'team',
        'status',
        'deadline',
        'created_at'
    )
    
    search_fields = (
        'title',
        'description',
    )
    
    list_filter = (
        'status',
        'deadline',
        'created_at',
        'team__project'
    )
    
    filter_horizontal = ('assignee',)


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = (
        'role_type',
        'user__username',
        'team__title',
    )
    
    search_fields = (
        'role_type',
    )
    
    list_filter = (
        'role_type',
        'user',
        'team',
    )
