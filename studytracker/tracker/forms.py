from django import forms
from .models import Attachment, ProgressLog, Reminder, StudySession, Subject, Task

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name']   # user will be auto assigned later


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['subject', 'title', 'description', 'deadline', 'priority', 'status', 'tags']
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'}),
            'tags': forms.SelectMultiple(attrs={'size': 5}),
        }

    def clean_priority(self):
        priority = self.cleaned_data.get('priority')
        if priority < 1 or priority > 5:
            raise forms.ValidationError("Priority must be between 1 and 5")
        return priority


class ProgressLogForm(forms.ModelForm):
    class Meta:
        model = ProgressLog
        fields = ['progress_percent']


class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ['file']


class ReminderForm(forms.ModelForm):
    reminder_time = forms.DateTimeField(
        input_formats=['%Y-%m-%dT%H:%M'],
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
    )

    class Meta:
        model = Reminder
        fields = ['reminder_time']


class StudySessionForm(forms.ModelForm):
    start_time = forms.DateTimeField(
        input_formats=['%Y-%m-%dT%H:%M'],
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
    )
    end_time = forms.DateTimeField(
        input_formats=['%Y-%m-%dT%H:%M'],
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
    )

    class Meta:
        model = StudySession
        fields = ['start_time', 'end_time']