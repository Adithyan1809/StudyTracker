from django import forms
from .models import Subject, Task

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name']   # user will be auto assigned later


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['subject', 'title', 'description', 'deadline', 'priority', 'status']

    def clean_priority(self):
        priority = self.cleaned_data.get('priority')
        if priority < 1 or priority > 5:
            raise forms.ValidationError("Priority must be between 1 and 5")
        return priority