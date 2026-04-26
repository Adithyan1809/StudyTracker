# 📚 Study Tracker

A full-stack web application built using **Django** and **PostgreSQL** to help students manage subjects, track tasks, and monitor progress through an intuitive dashboard.

---

## 🚀 Overview

Study Tracker is designed to simplify academic planning by organizing tasks under subjects, tracking completion progress, and highlighting deadlines.

### 🎯 Key Objectives

* Organize tasks subject-wise
* Track progress visually
* Identify overdue tasks
* Provide exportable reports (CSV & PDF)

---

## ✨ Features

### 🔐 Authentication

* Login-required access for all features
* User-specific data isolation using Django authentication

---

### 📚 Subject Management

* Create subjects linked to the logged-in user
* Instant feedback on successful creation

---

### ✅ Task Management

* Add, edit, delete tasks
* Mark tasks as completed
* Delete confirmation for safety

**Task Attributes:**

* Title
* Description
* Deadline
* Priority (1–5)
* Status (Pending / Completed)

---

### 📊 Dashboard & Analytics

* Real-time summary cards:

  * Total Tasks
  * Completed
  * Pending
  * Overdue
  * Progress (%)

* Interactive filtering via summary cards

* Intelligent status badges:

  * 🔴 Overdue
  * 🟡 Pending
  * 🟢 Completed

* Tasks sorted by:

  * Deadline → Priority

---

### 📤 Export Features

* Download tasks as **CSV**
* Generate **PDF reports**

---

### 🎨 User Interface

* Responsive modern dashboard
* Clean layout with shared header/footer
* User-friendly task actions

---

## 🛠️ Tech Stack

* **Backend:** Django 6.0.4 (Python 3.13)
* **Database:** PostgreSQL
* **Frontend:** Django Templates (HTML/CSS)
* **PDF Generation:** ReportLab

---

## 📁 Project Structure

```
StudyTracker/
│
├── README.md
├── requirements.txt
│
└── studytracker/
    ├── manage.py
    │
    ├── studytracker/
    │   ├── settings.py
    │   ├── urls.py
    │   ├── asgi.py
    │   └── wsgi.py
    │
    └── tracker/
        ├── models.py
        ├── views.py
        ├── forms.py
        ├── urls.py
        ├── admin.py
        ├── migrations/
        │
        └── templates/
            ├── base.html
            ├── dashboard.html
            ├── add_subject.html
            ├── add_task.html
            └── edit_task.html
```

---

## 🗄️ Data Model

### 📘 Subject

* `user` → ForeignKey (Django User)
* `name`
* `created_at`

---

### 📘 Task

* `subject` → ForeignKey (Subject)
* `title`
* `description`
* `deadline`
* `priority (1–5)`
* `status (pending/completed)`
* `created_at`

---

### 🔗 Relationships

* One **User** → Multiple **Subjects**
* One **Subject** → Multiple **Tasks**

---

## ⚙️ Setup & Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Adithyan1809/study-tracker.git
cd study-tracker
```

---

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Configure PostgreSQL

Update database settings in:

```
studytracker/settings.py
```

---

### 5️⃣ Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

### 6️⃣ Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

---

### 7️⃣ Run Server

```bash
python manage.py runserver
```

---

### 🌐 Open in Browser

```
http://127.0.0.1:8000/
```

---

## 🔗 Application Routes

| Route                  | Description        |
| ---------------------- | ------------------ |
| `/`                    | Dashboard          |
| `/add-subject/`        | Add Subject        |
| `/add-task/`           | Add Task           |
| `/edit-task/<id>/`     | Edit Task          |
| `/complete-task/<id>/` | Mark Task Complete |
| `/delete-task/<id>/`   | Delete Task        |
| `/export-csv/`         | Export CSV         |
| `/export-pdf/`         | Export PDF         |
| `/admin/`              | Django Admin Panel |

---

## ⚠️ Notes

* PostgreSQL is used as the primary database
* For production:

  * Use environment variables for credentials
  * Disable debug mode
  * Configure proper hosting (Gunicorn/Nginx)

---

## 🌟 Highlights

* Clean relational database design
* User-specific data handling
* Real-time analytics dashboard
* Export functionality (CSV & PDF)
* Practical full-stack implementation

---

## 👨‍💻 Team

* **Adithyan P**
* **Pavan Gowda K**
* **Pracheth Singh**

---

## 📌 Final Note

This project is built as part of academic coursework while focusing on real-world development practices, scalability, and usability.
