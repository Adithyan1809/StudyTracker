from django.shortcuts import render, redirect, get_object_or_404
from .forms import SubjectForm, TaskForm
from django.contrib.auth.decorators import login_required 
from .models import Subject, Task
import csv
from django.http import HttpResponse

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

@login_required
def mark_complete(request, task_id):
    task = get_object_or_404(Task, id=task_id, subject__user=request.user)
    task.status = 'completed'
    task.save()
    return redirect('dashboard')

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, subject__user=request.user)
    task.delete()
    return redirect('dashboard')



@login_required
def export_csv(request):
    tasks = Task.objects.filter(subject__user=request.user)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="tasks.csv"'

    writer = csv.writer(response)
    writer.writerow(['Title', 'Subject', 'Status', 'Deadline', 'Priority'])

    for task in tasks:
        writer.writerow([
            task.title,
            task.subject.name,
            task.status,
            task.deadline,
            task.priority
        ])

    return response

from reportlab.platypus import SimpleDocTemplate, Table
from django.http import HttpResponse

@login_required
def export_pdf(request):
    tasks = Task.objects.filter(subject__user=request.user)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="tasks.pdf"'

    doc = SimpleDocTemplate(response)

    data = [['Title', 'Subject', 'Status', 'Deadline', 'Priority']]

    for task in tasks:
        data.append([
            task.title,
            task.subject.name,
            task.status,
            str(task.deadline),
            task.priority
        ])

    table = Table(data)
    doc.build([table])

    return response