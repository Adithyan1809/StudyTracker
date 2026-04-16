from django.contrib import admin
from .models import Subject, Task


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user', 'created_at')
    search_fields = ('name',)
    list_filter = ('created_at',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'subject', 'priority', 'status', 'deadline')
    search_fields = ('title',)
    list_filter = ('status', 'priority', 'deadline')