from django.shortcuts import render, redirect
from .forms import SubjectForm, TaskForm
from django.contrib.auth.decorators import login_required 
from .models import Subject, Task
@login_required  
def add_subject(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            subject = form.save(commit=False)
            subject.user = request.user
            subject.save()
            return redirect('add-subject')
    else:
        form = SubjectForm()

    return render(request, 'add_subject.html', {'form': form})

@login_required
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        form.fields['subject'].queryset = Subject.objects.filter(user=request.user)

        if form.is_valid():
            form.save()
            return redirect('add-task')
    else:
        form = TaskForm()
        form.fields['subject'].queryset = Subject.objects.filter(user=request.user)

    return render(request, 'add_task.html', {'form': form})



@login_required
def dashboard(request):
    tasks = Task.objects.filter(subject__user=request.user)

    total_tasks = tasks.count()
    completed_tasks = tasks.filter(status='completed').count()
    pending_tasks = tasks.filter(status='pending').count()

    # Avoid division by zero
    progress = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0

    context = {
        'tasks': tasks,
        'total': total_tasks,
        'completed': completed_tasks,
        'pending': pending_tasks,
        'progress': round(progress, 2)
    }

    return render(request, 'dashboard.html', context)