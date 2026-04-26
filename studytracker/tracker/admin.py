from django.contrib import admin
from .models import Attachment, ProgressLog, Reminder, StudySession, Subject, Tag, Task


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


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(ProgressLog)
class ProgressLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'task', 'progress_percent', 'updated_at')
    list_filter = ('updated_at',)


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'task', 'uploaded_at')
    list_filter = ('uploaded_at',)


@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ('id', 'task', 'reminder_time', 'is_sent')
    list_filter = ('is_sent', 'reminder_time')


@admin.register(StudySession)
class StudySessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'task', 'start_time', 'end_time')
    list_filter = ('start_time', 'end_time')