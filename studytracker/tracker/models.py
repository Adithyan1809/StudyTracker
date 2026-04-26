from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

# Subject Model
class Subject(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# Task Model
class Task(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    ]

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    deadline = models.DateField()
    priority = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    tags = models.ManyToManyField(Tag, blank=True, related_name='tasks')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ProgressLog(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='progress_logs')
    progress_percent = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.task.title} - {self.progress_percent}%"


class Attachment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='attachments/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Attachment for {self.task.title}"


class Reminder(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='reminders')
    reminder_time = models.DateTimeField()
    is_sent = models.BooleanField(default=False)

    def __str__(self):
        return f"Reminder for {self.task.title} at {self.reminder_time}"


class StudySession(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='study_sessions')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(end_time__gt=models.F('start_time')),
                name='study_session_end_after_start',
            ),
        ]

    def __str__(self):
        return f"Session for {self.task.title}"
