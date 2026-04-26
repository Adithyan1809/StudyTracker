# Study Tracker

A Django + PostgreSQL web app to manage subjects, track study tasks, and monitor progress with an interactive dashboard.

## Overview

Study Tracker helps students organize work by subject and task.

Core goals:
- Keep tasks grouped by subject.
- Track completion progress clearly.
- Highlight overdue tasks.
- Export task data to CSV and PDF.

## Features

### Authentication
- Login-required access for all tracker features.
- User-specific data isolation using Django auth.

### Subject Management
- Add subjects linked to the logged-in user.
- Subject creation success feedback via popup and message.

### Task Management
- Add task.
- Edit task.
- Mark task complete.
- Delete task with confirmation prompt.
- Task fields:
  - Title
  - Description
  - Deadline
  - Priority (1-5)
  - Status (Pending/Completed)

### Dashboard and Analytics
- Task summary cards:
  - Total
  - Completed
  - Pending
  - Overdue
  - Progress percentage
- Clickable summary cards for status filtering.
- Deadline-aware status badges:
  - Overdue
  - Pending
  - Completed
- Tasks sorted by deadline, then priority.

### Export
- Export tasks as CSV.
- Export tasks as PDF.

### UI
- Responsive custom dashboard and forms.
- Shared header/footer layout.

## Tech Stack

- Python 3.13
- Django 6.0.4
- PostgreSQL
- Django templates (HTML/CSS)
- ReportLab (PDF export)

## Project Structure

```
StudyTracker/
  README.md
  requirements.txt
  studytracker/
    manage.py
    studytracker/
      settings.py
      urls.py
      asgi.py
      wsgi.py
    tracker/
      models.py
      views.py
      forms.py
      urls.py
      admin.py
      migrations/
      templates/
        base.html
        dashboard.html
        add_subject.html
        add_task.html
        edit_task.html
```

## Data Model

### Subject
- user -> ForeignKey to Django User
- name
- created_at

### Task
- subject -> ForeignKey to Subject
- title
- description
- deadline
- priority (1-5)
- status (pending/completed)
- created_at

### Relationships
- One User has many Subjects.
- One Subject has many Tasks.

## Requirements

Dependencies are listed in requirements.txt.

## Setup and Run

1. Create and activate a virtual environment.
2. Install dependencies.
3. Configure PostgreSQL database settings in studytracker/studytracker/settings.py.
4. Run migrations.
5. Create a superuser (optional, for admin).
6. Start the server.

Example commands:

```bash
cd studytracker
python -m pip install -r ../requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open in browser:

```text
http://127.0.0.1:8000/
```

## Main Routes

- / -> Dashboard
- /add-subject/ -> Add Subject
- /add-task/ -> Add Task
- /edit-task/<task_id>/ -> Edit Task
- /complete-task/<task_id>/ -> Mark Complete
- /delete-task/<task_id>/ -> Delete Task
- /export-csv/ -> CSV Export
- /export-pdf/ -> PDF Export
- /admin/ -> Django Admin

## Notes

- Project currently uses PostgreSQL in settings.
- For production usage, move secrets and DB credentials to environment variables.

## Team

Developed by:
- Adithyan P
- Pavan Gowda K
- Pracheth Singh

