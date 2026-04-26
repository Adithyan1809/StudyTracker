from django.shortcuts import render, redirect, get_object_or_404
from .forms import SubjectForm, TaskForm
from django.contrib.auth.decorators import login_required 
from .models import Subject, Task
import csv
from django.http import HttpResponse
from django.contrib import messages
from datetime import date

@login_required  
def add_subject(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            subject = form.save(commit=False)
            subject.user = request.user
            subject.save()
            messages.success(request, 'Subject added successfully.')
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
            messages.success(request, 'Task added successfully.')
            return redirect('dashboard')
    else:
        form = TaskForm()
        form.fields['subject'].queryset = Subject.objects.filter(user=request.user)

    return render(request, 'add_task.html', {'form': form})


@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, subject__user=request.user)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        form.fields['subject'].queryset = Subject.objects.filter(user=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully.')
            return redirect('dashboard')
    else:
        form = TaskForm(instance=task)
        form.fields['subject'].queryset = Subject.objects.filter(user=request.user)

    return render(request, 'edit_task.html', {'form': form, 'task': task})



@login_required
def dashboard(request):
    today = date.today()
    status_filter = request.GET.get('status', 'all')

    all_tasks = Task.objects.filter(subject__user=request.user).order_by('deadline', '-priority')
    tasks = all_tasks

    if status_filter == 'pending':
        tasks = all_tasks.filter(status='pending')
    elif status_filter == 'completed':
        tasks = all_tasks.filter(status='completed')
    elif status_filter == 'overdue':
        tasks = all_tasks.filter(status='pending', deadline__lt=today)

    total_tasks = all_tasks.count()
    completed_tasks = all_tasks.filter(status='completed').count()
    pending_tasks = all_tasks.filter(status='pending').count()
    overdue_tasks = all_tasks.filter(status='pending', deadline__lt=today).count()

    # Avoid division by zero
    progress = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0

    context = {
        'tasks': tasks,
        'total': total_tasks,
        'completed': completed_tasks,
        'pending': pending_tasks,
        'overdue': overdue_tasks,
        'progress': round(progress, 2),
        'today': today,
        'status_filter': status_filter,
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