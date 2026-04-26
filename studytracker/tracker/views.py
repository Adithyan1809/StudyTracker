from django.shortcuts import render, redirect, get_object_or_404
from .forms import AttachmentForm, ProgressLogForm, ReminderForm, StudySessionForm, SubjectForm, TaskForm
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Attachment, ProgressLog, Reminder, StudySession, Subject, Task
import csv
from django.http import HttpResponse
from django.contrib import messages
from datetime import date
from django.db.models import Case, IntegerField, Value, When


def signup(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully. Welcome!')
            return redirect('dashboard')
    else:
        form = UserCreationForm()

    return render(request, 'signup.html', {'form': form})

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
        form_type = request.POST.get('form_type', 'task')

        if form_type == 'task':
            form = TaskForm(request.POST, instance=task)
            form.fields['subject'].queryset = Subject.objects.filter(user=request.user)
            progress_form = ProgressLogForm()
            attachment_form = AttachmentForm()
            reminder_form = ReminderForm()
            session_form = StudySessionForm()

            if form.is_valid():
                form.save()
                messages.success(request, 'Task updated successfully.')
                return redirect('edit-task', task_id=task.id)

        elif form_type == 'progress':
            form = TaskForm(instance=task)
            form.fields['subject'].queryset = Subject.objects.filter(user=request.user)
            progress_form = ProgressLogForm(request.POST)
            attachment_form = AttachmentForm()
            reminder_form = ReminderForm()
            session_form = StudySessionForm()

            if progress_form.is_valid():
                progress_log = progress_form.save(commit=False)
                progress_log.task = task
                progress_log.save()
                messages.success(request, 'Progress log added.')
                return redirect('edit-task', task_id=task.id)

        elif form_type == 'attachment':
            form = TaskForm(instance=task)
            form.fields['subject'].queryset = Subject.objects.filter(user=request.user)
            progress_form = ProgressLogForm()
            attachment_form = AttachmentForm(request.POST, request.FILES)
            reminder_form = ReminderForm()
            session_form = StudySessionForm()

            if attachment_form.is_valid():
                attachment = attachment_form.save(commit=False)
                attachment.task = task
                attachment.save()
                messages.success(request, 'Attachment uploaded.')
                return redirect('edit-task', task_id=task.id)

        elif form_type == 'reminder':
            form = TaskForm(instance=task)
            form.fields['subject'].queryset = Subject.objects.filter(user=request.user)
            progress_form = ProgressLogForm()
            attachment_form = AttachmentForm()
            reminder_form = ReminderForm(request.POST)
            session_form = StudySessionForm()

            if reminder_form.is_valid():
                reminder = reminder_form.save(commit=False)
                reminder.task = task
                reminder.save()
                messages.success(request, 'Reminder added.')
                return redirect('edit-task', task_id=task.id)

        elif form_type == 'session':
            form = TaskForm(instance=task)
            form.fields['subject'].queryset = Subject.objects.filter(user=request.user)
            progress_form = ProgressLogForm()
            attachment_form = AttachmentForm()
            reminder_form = ReminderForm()
            session_form = StudySessionForm(request.POST)

            if session_form.is_valid():
                study_session = session_form.save(commit=False)
                study_session.task = task
                study_session.save()
                messages.success(request, 'Study session added.')
                return redirect('edit-task', task_id=task.id)

        else:
            form = TaskForm(instance=task)
            form.fields['subject'].queryset = Subject.objects.filter(user=request.user)
            progress_form = ProgressLogForm()
            attachment_form = AttachmentForm()
            reminder_form = ReminderForm()
            session_form = StudySessionForm()
    else:
        form = TaskForm(instance=task)
        form.fields['subject'].queryset = Subject.objects.filter(user=request.user)
        progress_form = ProgressLogForm()
        attachment_form = AttachmentForm()
        reminder_form = ReminderForm()
        session_form = StudySessionForm()

    context = {
        'form': form,
        'task': task,
        'progress_form': progress_form,
        'attachment_form': attachment_form,
        'reminder_form': reminder_form,
        'session_form': session_form,
        'progress_logs': task.progress_logs.order_by('-updated_at'),
        'attachments': task.attachments.order_by('-uploaded_at'),
        'reminders': task.reminders.order_by('reminder_time'),
        'study_sessions': task.study_sessions.order_by('-start_time'),
    }
    return render(request, 'edit_task.html', context)


@login_required
def delete_progress_log(request, log_id):
    progress_log = get_object_or_404(ProgressLog, id=log_id, task__subject__user=request.user)
    task_id = progress_log.task_id
    progress_log.delete()
    messages.success(request, 'Progress log removed.')
    return redirect('edit-task', task_id=task_id)


@login_required
def delete_attachment(request, attachment_id):
    attachment = get_object_or_404(Attachment, id=attachment_id, task__subject__user=request.user)
    task_id = attachment.task_id
    attachment.delete()
    messages.success(request, 'Attachment removed.')
    return redirect('edit-task', task_id=task_id)


@login_required
def delete_reminder(request, reminder_id):
    reminder = get_object_or_404(Reminder, id=reminder_id, task__subject__user=request.user)
    task_id = reminder.task_id
    reminder.delete()
    messages.success(request, 'Reminder removed.')
    return redirect('edit-task', task_id=task_id)


@login_required
def delete_study_session(request, session_id):
    study_session = get_object_or_404(StudySession, id=session_id, task__subject__user=request.user)
    task_id = study_session.task_id
    study_session.delete()
    messages.success(request, 'Study session removed.')
    return redirect('edit-task', task_id=task_id)



@login_required
def dashboard(request):
    today = date.today()
    status_filter = request.GET.get('status', 'all')
    priority_filter = request.GET.get('priority', 'all')
    subject_filter = request.GET.get('subject', 'all')
    sort_by = request.GET.get('sort', 'smart')

    base_tasks = Task.objects.filter(subject__user=request.user)
    all_tasks = base_tasks.annotate(
        status_rank=Case(
            When(status='completed', then=Value(1)),
            default=Value(0),
            output_field=IntegerField(),
        )
    )
    tasks = all_tasks

    if status_filter == 'pending':
        tasks = tasks.filter(status='pending')
    elif status_filter == 'completed':
        tasks = tasks.filter(status='completed')
    elif status_filter == 'overdue':
        tasks = tasks.filter(status='pending', deadline__lt=today)

    if priority_filter in {'1', '2', '3', '4', '5'}:
        tasks = tasks.filter(priority=int(priority_filter))

    if subject_filter.isdigit():
        tasks = tasks.filter(subject_id=int(subject_filter))

    if sort_by == 'deadline_desc':
        tasks = tasks.order_by('status_rank', '-deadline', '-priority')
    elif sort_by == 'priority_high':
        tasks = tasks.order_by('status_rank', '-priority', 'deadline')
    elif sort_by == 'priority_low':
        tasks = tasks.order_by('status_rank', 'priority', 'deadline')
    elif sort_by == 'created_desc':
        tasks = tasks.order_by('status_rank', '-created_at')
    elif sort_by == 'created_asc':
        tasks = tasks.order_by('status_rank', 'created_at')
    else:
        tasks = tasks.order_by('status_rank', 'deadline', '-priority')

    total_tasks = base_tasks.count()
    completed_tasks = base_tasks.filter(status='completed').count()
    pending_tasks = base_tasks.filter(status='pending').count()
    overdue_tasks = base_tasks.filter(status='pending', deadline__lt=today).count()

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
        'priority_filter': priority_filter,
        'subject_filter': subject_filter,
        'sort_by': sort_by,
        'subjects': Subject.objects.filter(user=request.user).order_by('name'),
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