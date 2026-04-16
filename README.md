# 📚 Study Tracker (Django + PostgreSQL)

##  Project Overview

Study Tracker is a web-based application built using **Django** and **PostgreSQL** that helps students manage their subjects, track study tasks, and monitor progress efficiently.

This project is developed as part of coursework, with a focus on practical application of Django fundamentals.

---

## 🎯 Features Implemented

### 🔐 User Authentication
- Login required to access core features
- Session-based authentication using Django

### 📚 Subject Management
- Add subjects for each user
- Each subject is linked to a specific user

### ✅ Task Management
- Add tasks under subjects
- Fields:
  - Title
  - Description
  - Deadline
  - Priority (1–5)
  - Status (Pending/Completed)

### 📊 Dashboard (Analytics)
- View all tasks in a structured table
- Displays:
  - Total tasks
  - Completed tasks
  - Pending tasks
  - Progress percentage

### ⚙️ Admin Panel
- Manage users, subjects, and tasks
- Search, filter, and view data efficiently

---


## 🗄️ Database Design

### 🔹 Entities:
- User (Django built-in)  
- Subject  
- Task  

### 🔹 Relationships:
- One User → Many Subjects  
- One Subject → Many Tasks  

---

## 🛠️ Tech Stack

- **Backend:** Django (Python)  
- **Database:** PostgreSQL  
- **Frontend:** HTML (Django Templates)  
- **ORM:** Django ORM  

---

